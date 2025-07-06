package com.example.myproject;

import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.android.volley.DefaultRetryPolicy;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.RetryPolicy;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.example.myproject.Adapter.Message;
import com.example.myproject.Adapter.MessageAdapter;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Date;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import androidx.appcompat.widget.Toolbar;
import android.Manifest;
import io.socket.client.IO;
import io.socket.client.Socket;
import io.socket.emitter.Emitter;
import androidx.recyclerview.widget.LinearLayoutManager;

public class ChatActivity extends AppCompatActivity {

    private List<Message> messageList = new ArrayList<>(); // 訊息列表
    private MessageAdapter messageAdapter; // 訊息適配器
    private RequestQueue requestQueue; // 請求隊列
    private Button btnConfirm; // 確認按鈕
    private Socket mSocket;
    private LinearLayoutManager layoutManager; // 類別層級變數


    @Override
    protected void onDestroy() {
        super.onDestroy();
        // 通過 SocketApplication 統一管理斷開連接
        Log.d("ChatActivity", "ChatActivity 被銷毀，但 Socket 連線保持開啟。");
//        SocketApplication app = (SocketApplication) getApplication();
//        app.disconnectSocket(); // 使用統一的斷開邏輯
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chat);


        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        toolbar.setNavigationOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // 返回到AssistentFragment
                finish();
            }
        });

        RecyclerView recyclerView = findViewById(R.id.recycler_view);
        layoutManager = new LinearLayoutManager(this); // 初始化 layoutManager
        layoutManager.setStackFromEnd(true); // 確保從底部開始顯示
        recyclerView.setLayoutManager(layoutManager); // 設置到 RecyclerView


        messageAdapter = new MessageAdapter(messageList, this::handleConfirmButtonClick);
        recyclerView.setAdapter(messageAdapter);


        // 獲取全局 Socket 實例
        SocketApplication app = (SocketApplication) getApplication();
        mSocket = app.getSocket();
        mSocket.on(Socket.EVENT_CONNECT, onConnect);
        mSocket.on("restaurant_list", onRestaurantList);
        mSocket.on("message", onNewMessage);
        mSocket.on("navigate_to_address", onNavigateToAddress);
        mSocket.on("recommendation_list", onRecommendationList);
        mSocket.on(Socket.EVENT_DISCONNECT, onDisconnect);

        // 初始化訊息列表
        initializeMessageList();

        recyclerView.scrollToPosition(messageList.size() - 1); // 初始化後滾動到最底部

        EditText etMessage = findViewById(R.id.et_message);
        Button btnSend = findViewById(R.id.btn_send);
        btnSend.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String messageText = etMessage.getText().toString();
                if (!messageText.isEmpty()) {
                    String timestamp = getCurrentTimestamp();
                    messageList.add(new Message(messageText, timestamp, true, true, false, false, null)); // 添加用戶發送的訊息到列表
                    messageAdapter.notifyItemInserted(messageList.size() - 1); // 使用 notifyItemInserted


                    // 滾動到最底部
                    recyclerView.scrollToPosition(messageList.size() - 1);

                    etMessage.setText(""); // 清空輸入框

                    // 發送用戶消息到伺服器獲取AI回應
                    sendMessageToServer(messageText);
                }
            }
        });

        btnConfirm = findViewById(R.id.btn_confirm);
        btnConfirm.setOnClickListener(this::handleConfirmButtonClick);

    }

    // 監聽 Socket.IO 連接成功
    private Emitter.Listener onConnect = args -> runOnUiThread(() ->
            Toast.makeText(ChatActivity.this, "已連接至伺服器", Toast.LENGTH_SHORT).show()
    );


    // 可以刪除 Toast 提示，但保留對斷開事件的監聽
    private Emitter.Listener onDisconnect = args -> runOnUiThread(() -> {
        // 可以選擇不顯示 Toast 提示，僅記錄日誌
        Log.d("ChatActivity", "Socket 已斷開連接");
    });


    private Emitter.Listener onRecommendationList = args -> runOnUiThread(() -> {
        try {
            // 確保 args[0] 是 JSONObject
            JSONObject data = (JSONObject) args[0];
            Log.d("onRecommendationList", "收到的原始數據: " + data.toString());

            // 提取 "recommendations" 的值
            String recommendedStore = data.getString("recommendations");
            Log.d("onRecommendationList", "接收到推薦餐廳: " + recommendedStore);

            // 添加到訊息列表
            String timestamp = getCurrentTimestamp();
            messageList.add(new Message("我覺得你可能會喜歡：" + recommendedStore, timestamp, false, true, false, false, null));
            messageAdapter.notifyItemInserted(messageList.size() - 1);
        } catch (JSONException e) {
            e.printStackTrace();
            Log.e("onRecommendationList", "解析推薦餐廳失敗: " + e.getMessage());
        }
    });




    // 監聽 navigate_to_address 事件，並導航至 Google Maps
    private Emitter.Listener onNavigateToAddress = args -> runOnUiThread(() -> {
        try {
            JSONObject data = (JSONObject) args[0];
            String address = data.getString("address");  // 從 JSON 中取得地址

            // 使用 Intent 啟動 Google Maps 進行導航
            Uri gmmIntentUri = Uri.parse("geo:0,0?q=" + Uri.encode(address));
            Intent mapIntent = new Intent(Intent.ACTION_VIEW, gmmIntentUri);
            mapIntent.setPackage("com.google.android.apps.maps");  // 指定使用 Google Maps

            // 確認 Google Maps 是否存在
            if (mapIntent.resolveActivity(getPackageManager()) != null) {
                startActivity(mapIntent);  // 啟動 Google Maps
            } else {
                Toast.makeText(ChatActivity.this, "無法啟動導航，請安裝 Google Maps", Toast.LENGTH_SHORT).show();
            }

        } catch (JSONException e) {
            e.printStackTrace();
            Toast.makeText(ChatActivity.this, "導航地址無效", Toast.LENGTH_SHORT).show();
        }
    });

    private Emitter.Listener onNewMessage = args -> runOnUiThread(() -> {
        try {
            Object data = args[0];
            String aiResponse;

            if (data instanceof JSONObject) {
                JSONObject jsonObject = (JSONObject) data;
                aiResponse = jsonObject.getString("reply");
            } else {
                aiResponse = (String) data;
            }

            String timestamp = getCurrentTimestamp();
            messageList.add(new Message("AI回應: " + aiResponse, timestamp, false, true, false, false, null));
            messageAdapter.notifyItemInserted(messageList.size() - 1);
        } catch (JSONException e) {
            e.printStackTrace();
        }
    });




    // 監聽餐廳列表
    private Emitter.Listener onRestaurantList = args -> runOnUiThread(() -> {
        try {
            JSONObject data = (JSONObject) args[0];
            List<String> restaurantList = new ArrayList<>();
            JSONArray restaurantArray = data.getJSONArray("restaurants");

            for (int i = 0; i < restaurantArray.length(); i++) {
                restaurantList.add(restaurantArray.getString(i));
            }

            String timestamp = getCurrentTimestamp();
            messageList.add(new Message("請選擇以下餐廳編號：", timestamp, false, false, true, false, restaurantList));
            btnConfirm.setVisibility(View.VISIBLE);
            messageAdapter.notifyDataSetChanged();
        } catch (JSONException e) {
            e.printStackTrace();
        }
    });

    // 使用 Socket.IO 發送訊息到伺服器，並處理撥打電話的特殊指令
    private void sendMessageToServer(String messageText) {
            // 若無需撥打電話，則將訊息發送到伺服器
            mSocket.emit("message", messageText);
    }

    private void initializeMessageList() {
        String timestamp = getCurrentTimestamp();
        messageList.add(new Message("歡迎使用本應用!!", timestamp, false, false, false, false, null)); // 初始化歡迎訊息
    }


    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == 1) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                // 用戶授予了權限，重新執行撥打電話邏輯
                String phoneNumber = "0123456789"; // 替換成店家的真實電話號碼
                Intent callIntent = new Intent(Intent.ACTION_CALL);
                callIntent.setData(Uri.parse("tel:" + phoneNumber));
                if (ActivityCompat.checkSelfPermission(this, Manifest.permission.CALL_PHONE) == PackageManager.PERMISSION_GRANTED) {
                    startActivity(callIntent);
                }
            } else {
                // 用戶拒絕授予權限，提示
                Toast.makeText(this, "撥打電話需要授予撥打電話的權限", Toast.LENGTH_SHORT).show();
            }
        }
    }


    private void handleConfirmButtonClick(View view) {
        String selectedRestaurant = null;

        // 找到被選中的餐廳
        for (Message msg : messageList) {
            if (msg.isRestaurantList() && msg.getSelectedRestaurant() != null) {
                selectedRestaurant = msg.getSelectedRestaurant();
                break;
            }
        }

        if (selectedRestaurant != null) {
            String timestamp = getCurrentTimestamp();

            // 將選擇的餐廳作為使用者的氣泡新增到聊天界面
            messageList.add(new Message("選擇的餐廳是：" + selectedRestaurant, timestamp, true, false, false, false, Collections.emptyList()));
            messageAdapter.notifyDataSetChanged();

            // 發送消息到 Python 伺服器
            mSocket.emit("message", "選擇的餐廳是：" + selectedRestaurant);
        } else {
            Toast.makeText(this, "請選擇一個餐廳", Toast.LENGTH_SHORT).show();
        }

        // 隱藏所有指示器和確認按鈕
        for (Message msg : messageList) {
            msg.setShowIndicator(false); // 隱藏指示器
            msg.setShowConfirmButton(false);
            msg.setSelectedRestaurant(null); // 清除選擇狀態
        }

        btnConfirm.setVisibility(View.GONE);
        messageAdapter.notifyDataSetChanged();
    }




    private String getCurrentTimestamp() {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault());
        return sdf.format(new Date()); // 獲取當前時間戳
    }
}