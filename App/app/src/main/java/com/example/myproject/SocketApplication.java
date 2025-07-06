package com.example.myproject;

import android.app.Application;
import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

import io.socket.client.IO;
import io.socket.client.Socket;

public class SocketApplication extends Application {
    private Socket mSocket;

    @Override
    public void onCreate() {
        super.onCreate();
        try {
            mSocket = IO.socket("https://subdomain3.jp.ngrok.io"); // 替換為您的伺服器 URL
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public Socket getSocket() {
        return mSocket;
    }

    public void connectSocket(final String username, final String gender) {
        if (mSocket != null && !mSocket.connected()) {
            mSocket.connect();
            mSocket.on(Socket.EVENT_CONNECT, args -> {
                Log.d("SocketApplication", "Socket connected");

                // 在連接成功後立即發送資料
                sendUserDataToPython(username, gender);
            });
        }
    }

    public void disconnectSocket() {
        if (mSocket != null && mSocket.connected()) {
            mSocket.disconnect();
            Log.d("SocketApplication", "Socket disconnected");
        }
    }

    public boolean isSocketConnected() {
        return mSocket != null && mSocket.connected();
    }

    private void sendUserDataToPython(String username, String gender) {
        if (isSocketConnected()) {
            try {
                JSONObject data = new JSONObject();
                data.put("username", username);
                data.put("gender", gender);
                mSocket.emit("user_info", data);
                Log.d("SocketApplication", "Data sent to Python: " + data.toString());
            } catch (JSONException e) {
                e.printStackTrace();
                Log.e("SocketApplication", "Error sending data to Python", e);
            }
        } else {
            Log.e("SocketApplication", "Socket is not connected from SendUserData");
        }
    }
}
