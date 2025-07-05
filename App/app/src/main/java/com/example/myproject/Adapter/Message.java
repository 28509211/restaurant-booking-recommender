package com.example.myproject.Adapter;

import java.util.List;

public class Message {
    private String text;
    private String timestamp;
    private boolean isUserMessage;
    private boolean showTimestamp;
    private boolean isRestaurantList;
    private boolean isSelected;
    private boolean showConfirmButton;
    private boolean showIndicator; // 添加 showIndicator
    private String selectedRestaurant;
    private List<String> listItems; // 新增列表項目

    public Message(String text, String timestamp, boolean isUserMessage, boolean showTimestamp, boolean isRestaurantList, boolean showConfirmButton, List<String> listItems) {
        this.text = text;
        this.timestamp = timestamp;
        this.isUserMessage = isUserMessage;
        this.showTimestamp = showTimestamp;
        this.isRestaurantList = isRestaurantList;
        this.showConfirmButton = showConfirmButton;
        this.listItems = listItems;
        this.showIndicator = true; // 默認顯示指示器
    }

    public String getText() {
        return text;
    }

    public String getTimestamp() {
        return timestamp;
    }

    public boolean isUserMessage() {
        return isUserMessage;
    }

    public boolean isShowTimestamp() {
        return showTimestamp;
    }

    public boolean isRestaurantList() {
        return isRestaurantList;
    }

    public boolean isSelected() {
        return isSelected;
    }

    public void setSelected(boolean selected) {
        isSelected = selected;
    }

    public boolean isShowConfirmButton() {
        return showConfirmButton;
    }

    public void setShowConfirmButton(boolean showConfirmButton) {
        this.showConfirmButton = showConfirmButton;
    }

    public List<String> getListItems() {
        return listItems;
    }

    public void setListItems(List<String> listItems) {
        this.listItems = listItems;
    }

    public boolean isShowIndicator() {
        return showIndicator;
    }

    public void setShowIndicator(boolean showIndicator) {
        this.showIndicator = showIndicator;
    }

    public String getSelectedRestaurant() {
        return selectedRestaurant;
    }

    public void setSelectedRestaurant(String selectedRestaurant) {
        this.selectedRestaurant = selectedRestaurant;
    }
}