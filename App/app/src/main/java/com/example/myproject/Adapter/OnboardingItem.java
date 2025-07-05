package com.example.myproject.Adapter;

public class OnboardingItem {

    private int animationRes; // 新增用於儲存 Lottie 動畫資源的屬性
    private String title;
    private String description;

    public int getAnimationRes() {
        return animationRes;
    }

    public void setAnimationRes(int animationRes) {
        this.animationRes = animationRes;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }
}
