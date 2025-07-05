package com.example.myproject.Adapter;

import java.util.List;

public class FoodItem {
    private int storeId;
    private String storeName;
    private String category;
    private String address;
    private float ratings;
    private String service;
    private List<StoreHours> storeHours;
    private String imageUrl;

    public FoodItem(String storeName, String category, String address, float ratings, String service, List<StoreHours> storeHours, String imageUrl) {
        this.storeName = storeName;
        this.category = category;
        this.address = address;
        this.ratings = ratings;
        this.service = service;
        this.storeHours = storeHours;
        this.imageUrl = imageUrl;
    }

    // Getters and setters...

    public int getStoreId() {
        return storeId;
    }

    public void setStoreId(int storeId) {
        this.storeId = storeId;
    }

    public String getStoreName() {
        return storeName;
    }

    public void setStoreName(String storeName) {
        this.storeName = storeName;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public float getRatings() {
        return ratings;
    }

    public void setRatings(float ratings) {
        this.ratings = ratings;
    }

    public String getService() {
        return service;
    }

    public void setService(String service) {
        this.service = service;
    }

    public List<StoreHours> getStoreHours() {
        return storeHours;
    }

    public void setStoreHours(List<StoreHours> storeHours) {
        this.storeHours = storeHours;
    }

    public String getImageUrl() {
        return imageUrl;
    }

    public void setImageUrl(String imageUrl) {
        this.imageUrl = imageUrl;
    }
}
