package com.example.myproject;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.example.myproject.MainActivity;
import com.google.android.material.card.MaterialCardView;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class InterestSelectActivity extends AppCompatActivity {

    MaterialCardView selectCard ;
    TextView FoodType ;

    Button Getstarted ;
    boolean [] selectedFood ;
    ArrayList<Integer> foodList = new ArrayList<>() ;
    String [] foodArray = {"中式", "台式", "越式","韓式","日式", "美式", "丼飯",
            "義式",
            "菲律賓菜",
            "紫米粑粑",
            "輕食",
            "早餐",
            "紅龜粿",
            "串燒",
            "餛飩",
            "拌麵",
            "古早味",
            "牛奶冰",
            "米線",
            "馬打滾",
            "椰子汁",
            "咖啡廳",
            "牛肉飯",
            "牛丼",
            "包子",
            "饅頭",
            "滬菜",
            "港點",
            "豬腳",
            "紹子麵",
            "土魠魚羹",
            "熱炒",
            "肉排三明治",
            "酸辣麵",
            "雞湯",
            "雲南",
            "雞排",
            "鐵路便當",
            "烤物",
            "壽司",
            "水餃",
            "盒飯",
            "拉麵",
            "甜點",
            "鹹酥雞",
            "油條",
            "麻辣鍋",
            "泰式奶茶",
            "便當",
            "牛排",
            "休閒",
            "飲料",
            "義大利麵",
            "菲律賓式",
            "黃悶雞",
            "麻辣臭豆腐",
            "炸雞",
            "打拋肉",
            "麻辣滷味",
            "炒米粉",
            "蔥油餅",
            "蒸餃",
            "迴轉壽司",
            "台式牛排",
            "咖哩飯",
            "烤雞",
            "油飯",
            "傳統",
            "仙草凍",
            "磚窯雞",
            "叻沙",
            "甜品",
            "臭豆腐",
            "粽子",
            "碳烤雞腿",
            "粉圓",
            "日式",
            "三杯雞",
            "石頭火鍋",
            "三明治",
            "印尼風",
            "砂鍋",
            "韭菜盒",
            "炸物",
            "沙拉",
            "海鮮",
            "disqualified",
            "泡菜",
            "和式",
            "米粉",
            "章魚燒",
            "健康",
            "魷魚羹",
            "芭蕉粽",
            "玉里麵",
            "網美",
            "陽春麵",
            "大阪燒",
            "控肉飯",
            "異國料理",
            "甜不辣",
            "蚵仔煎",
            "居酒屋",
            "螺螄粉",
            "快炒",
            "南洋料理",
            "藥燉土虱",
            "越南河粉",
            "蔬食",
            "羹麵",
            "雞肉飯",
            "甕缸雞",
            "麻辣",
            "燒肉",
            "早午餐",
            "牛筋麵",
            "未分類",
            "排骨",
            "牛扒烀",
            "麵線",
            "優格",
            "清粥小菜",
            "粥",
            "素食便當",
            "泰式",
            "米糕",
            "燒仙草",
            "雲泰",
            "大腸麵線",
            "飲品",
            "炒麵",
            "米漿",
            "咖椰吐司",
            "生魚片",
            "蔥抓餅",
            "鐵板麵",
            "湯麵",
            "小火鍋",
            "鹹水雞",
            "海南雞",
            "小籠湯包",
            "焗烤",
            "小籠包",
            "山東大餅",
            "薑母鴨",
            "燒肉飯",
            "火鍋",
            "冰品",
            "烤串",
            "大薄片",
            "異國風情",
            "活蝦",
            "河粉",
            "咖啡",
            "胡椒湯",
            "赤肉羹",
            "粉粿",
            "米干",
            "肉羹",
            "帕尼尼",
            "黑白切",
            "肉圓",
            "燒餅",
            "麻辣燙",
            "客家菜",
            "定食",
            "水煎包",
            "啤酒",
            "粑粑絲",
            "素肉",
            "牛干巴",
            "辣炒牛肉",
            "鴨肉飯",
            "豆花",
            "麻油雞",
            "雞腿飯",
            "炸豬排",
            "雞蛋糕",
            "烤餅",
            "歐蕾",
            "法式吐司",
            "炒麵麵包",
            "蛋餅",
            "鴨肉冬粉",
            "披薩",
            "椰漿飯",
            "素食",
            "鐵板",
            "胡椒蔥餅",
            "燴飯",
            "吐司",
            "烤肉",
            "烏龍麵",
            "越式",
            "滷味",
            "涼拌木瓜",
            "肉粽",
            "羹湯",
            "快餐",
            "法國麵包",
            "韓式炸雞",
            "鐵板燒",
            "炭烤",
            "吃到飽",
            "三杯滷味",
            "破酥包",
            "煎包",
            "窯烤披薩",
            "丹麥吐司",
            "酥餅",
            "豆漿",
            "咖哩",
            "煎餃",
            "燒烤",
            "廣東粥",
            "生春捲",
            "韓式",
            "美式",
            "關東煮",
            "酸辣粉",
            "漢堡",
            "甕仔雞",
            "鵝肉飯",
            "鴨香飯",
            "可頌",
            "牛肉麵",
            "船麵",
            "小吃",
            "草粿",
            "布里歐",
            "燒臘",
            "桶仔雞",
            "鬆餅",
            "打拋雞",
            "印度菜",
            "鍋燒麵",
            "海苔飯捲",
            "墨西哥式",
            "涼麵",
            "自助餐",
            "豬血湯",
            "鮮魚",
            "薄餅",
            "螃蟹",
            "仙草",
            "粄條",
            "月亮蝦餅",
            "中式",
            "清真",
            "寵物友善",
            "炕肉販",
            "簡餐",
            "炒飯",
            "腸粉",
            "牛肉湯",
            "排骨酥",
            "新加坡菜",
            "下午茶",
            "排骨飯",
            "川菜",
            "豆粉",
            "乾麵",
            "羊肉羹",
            "飯糰",
            "炸醬麵",
            "健康餐",
            "傳統早餐",
            "鍋貼",
            "茶飲",
            "豬腳飯"  } ;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_interest_select);

        // intitial
        selectCard = findViewById(R.id.SelectCard) ;
        FoodType = findViewById(R.id.FoodType) ;
        selectedFood = new boolean[foodArray.length];
        Getstarted = findViewById(R.id.GetStarted) ;
        Getstarted.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                openMainActivity() ;
            }
        });

        selectCard.setOnClickListener(v -> {
            showFoodDialog() ;
        });
    }

    private void showFoodDialog(){
        AlertDialog.Builder builder = new AlertDialog.Builder(InterestSelectActivity.this);

        builder.setTitle("選擇喜歡的食物類型");
        builder.setCancelable(false);

        builder.setMultiChoiceItems(foodArray, selectedFood, new DialogInterface.OnMultiChoiceClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which, boolean isChecked) {
                if( isChecked ){
                    foodList.add(which);
                }
                else{
                    foodList.remove(Integer.valueOf(which)); // 從後往前刪除元素
                }

            }
        }).setPositiveButton("OK", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {

                //create stringbuilder
                StringBuilder stringBuilder = new StringBuilder();
                for( int i = 0 ; i < foodList.size() ; i++ ){
                    stringBuilder.append(foodArray[foodList.get(i)]);

                    //when not eqaul to foodlistsize then add coma
                    if( i != foodList.size() - 1 ){
                        stringBuilder.append(", ");

                    } // if

                    // setting selected food to textview
                    FoodType.setText(stringBuilder.toString());

                } // for
                RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
                String url ="https://subdomain1.jp.ngrok.io/login-register-android/initselect.php";
                StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
                        new Response.Listener<String>() {
                            @Override
                            public void onResponse(String response) {
                                Log.d("Response", response);
                            }
                        }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Log.e("Error", error.toString());
                    }
                }){
                    protected Map<String, String> getParams(){
                        Map<String, String> paramV = new HashMap<>();
                        paramV.put("initselect", stringBuilder.toString());
                        // 獲取 id
                        SharedPreferences sharedPreferences = getSharedPreferences("MyPrefs", MODE_PRIVATE);
                        String id = sharedPreferences.getString("id", null);
                        paramV.put("client_id", id);  // 添加 id 參數
                        return paramV;
                    }
                };
                queue.add(stringRequest);

            }
        }).setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                dialog.dismiss();

            }
        }).setNeutralButton("Clear all", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                for( int i = 0 ; i < selectedFood.length ; i ++ ){
                    selectedFood[i] = false ;
                    foodList.clear();
                    FoodType.setText("");

                } // for

            }
        });
        builder.show();
    }

    public void openMainActivity(){
        Intent intent = new Intent(this, MainActivity.class);
        startActivity(intent);
        finish();
    }
}
