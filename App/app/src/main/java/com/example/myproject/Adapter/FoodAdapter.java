package com.example.myproject.Adapter;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.bumptech.glide.Glide;
import com.example.myproject.R;
import com.example.myproject.StoreDetailActivity;

import java.util.ArrayList;
import java.util.List;

public class FoodAdapter extends RecyclerView.Adapter<FoodAdapter.FoodViewHolder> {

    private List<FoodItem> foodItemList;
    private Context context;

    public FoodAdapter(List<FoodItem> foodItemList, Context context) {
        this.foodItemList = foodItemList;
        this.context = context;
    }

    @NonNull
    @Override
    public FoodViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_food, parent, false);
        return new FoodViewHolder(view);
    }

    private String formatTime(String time) {
        if (time != null && !time.isEmpty()) {
            String[] parts = time.split(":");
            if (parts.length >= 2) {
                return parts[0] + ":" + parts[1]; // 只保留小時和分鐘
            }
        }
        return time; // 返回原始時間（若無法格式化）
    }

    @Override
    public void onBindViewHolder(@NonNull final FoodViewHolder holder, int position) {
        final FoodItem foodItem = foodItemList.get(position);
        holder.titleTxt.setText(foodItem.getStoreName());
        holder.startxt.setText(String.valueOf(foodItem.getRatings()));

        List<StoreHours> storeHoursList = foodItem.getStoreHours();
        if (!storeHoursList.isEmpty()) {
            StoreHours todayHours = storeHoursList.get(0);
            String hours = formatTime(todayHours.getOpenTime1()) + " - " + formatTime(todayHours.getCloseTime1());
            if (!todayHours.getOpenTime2().isEmpty() && !todayHours.getCloseTime2().isEmpty()) {
                hours += ", " + formatTime(todayHours.getOpenTime2()) + " - " + formatTime(todayHours.getCloseTime2());
            }
            holder.timeTxt.setText(hours);
        } else {
            holder.timeTxt.setText("No hours available");
        }

        // 使用 Glide 下載圖片
        Glide.with(context).load(foodItem.getImageUrl()).placeholder(R.drawable.ic_placeholder).into(holder.pic);

        // 點擊事件
        holder.pic.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(context, StoreDetailActivity.class);
                intent.putExtra("storeName", foodItem.getStoreName());
                intent.putExtra("category", foodItem.getCategory());
                intent.putExtra("address", foodItem.getAddress());
                intent.putExtra("ratings", foodItem.getRatings());
                intent.putExtra("service", foodItem.getService());
                intent.putParcelableArrayListExtra("storeHours", new ArrayList<>(foodItem.getStoreHours()));
                intent.putExtra("imageURL", foodItem.getImageUrl());
                context.startActivity(intent);
            }
        });

        // 設置愛心圖標的點擊事件
        boolean isFavorite = getFavoriteStatus(foodItem.getStoreName());
        updateFavoriteIcon(holder.favoriteImageView, isFavorite);

        holder.favoriteImageView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                boolean isFavorite = toggleFavoriteStatus(foodItem.getStoreName());
                updateFavoriteIcon(holder.favoriteImageView, isFavorite);
            }
        });
    }

    @Override
    public int getItemCount() {
        return foodItemList.size();
    }

    static class FoodViewHolder extends RecyclerView.ViewHolder {
        TextView titleTxt, startxt, timeTxt;
        ImageButton pic;
        ImageView imageView4, imageView5, favoriteImageView;

        public FoodViewHolder(@NonNull View itemView) {
            super(itemView);
            titleTxt = itemView.findViewById(R.id.titleTxt);
            startxt = itemView.findViewById(R.id.startxt);
            timeTxt = itemView.findViewById(R.id.timeTxt);
            pic = itemView.findViewById(R.id.pic);
            imageView4 = itemView.findViewById(R.id.imageView4);
            imageView5 = itemView.findViewById(R.id.imageView5);
            favoriteImageView = itemView.findViewById(R.id.favoriteImageView);
        }
    }

    private boolean getFavoriteStatus(String storeName) {
        SharedPreferences sharedPreferences = context.getSharedPreferences("MyPrefs", Context.MODE_PRIVATE);
        return sharedPreferences.getBoolean(storeName, false);
    }

    private boolean toggleFavoriteStatus(String storeName) {
        SharedPreferences sharedPreferences = context.getSharedPreferences("MyPrefs", Context.MODE_PRIVATE);
        boolean isFavorite = sharedPreferences.getBoolean(storeName, false);
        SharedPreferences.Editor editor = sharedPreferences.edit();
        editor.putBoolean(storeName, !isFavorite);
        editor.apply();
        return !isFavorite;
    }

    private void updateFavoriteIcon(ImageView favoriteImageView, boolean isFavorite) {
        if (isFavorite) {
            favoriteImageView.setImageResource(R.drawable.baseline_favorite_24);
        } else {
            favoriteImageView.setImageResource(R.drawable.baseline_favorite_border_24);
        }
    }
}
