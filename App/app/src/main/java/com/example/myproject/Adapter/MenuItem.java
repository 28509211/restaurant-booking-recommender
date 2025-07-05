package com.example.myproject.Adapter;

public class MenuItem {
    private int productId;
    private int storeId;
    private String productName;
    private String description;
    private int price;

    public MenuItem(int productId, int storeId, String productName, String description, int price) {
        this.productId = productId;
        this.storeId = storeId;
        this.productName = productName;
        this.description = description;
        this.price = price;
    }

    // Getter methods
    public int getProductId() {
        return productId;
    }

    public int getStoreId() {
        return storeId;
    }

    public String getProductName() {
        return productName;
    }

    public String getDescription() {
        return description;
    }

    public int getPrice() {
        return price;
    }
}
