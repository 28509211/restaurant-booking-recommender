package com.example.myproject;

public class ChatMessage {
    private String message;
    private String timestamp;

    public ChatMessage(String message, String timestamp) {
        this.message = message;
        this.timestamp = timestamp;
    }

    public String getMessage() {
        return message;
    }

    public String getTimestamp() {
        return timestamp;
    }
}
