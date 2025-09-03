package com.example.myproject;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import com.bumptech.glide.Glide;
import com.example.myproject.Adapter.StoreHours;

import java.util.List;

public class StoreDetailActivity extends AppCompatActivity {

    private TextView storeNameTxt, categoryTxt, addressTxt, ratingsTxt, serviceTxt, hoursTxt;
    private ImageView storeImageView;
    private Button orderButton;
    private ImageButton backButton;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_store_detail);

        storeNameTxt = findViewById(R.id.storeNameTxt);
        categoryTxt = findViewById(R.id.categoryTxt);
        addressTxt = findViewById(R.id.addressTxt);
        ratingsTxt = findViewById(R.id.ratingsTxt);
        serviceTxt = findViewById(R.id.serviceTxt);
        hoursTxt = findViewById(R.id.hoursTxt);
        storeImageView = findViewById(R.id.storeImageView);
        orderButton = findViewById(R.id.orderButton);
        backButton = findViewById(R.id.backButton);

        // 获取传递的店家信息
        Bundle extras = getIntent().getExtras();
        if (extras != null) {
            String storeName = extras.getString("storeName");
            String category = extras.getString("category");
            String address = extras.getString("address");
            float ratings = extras.getFloat("ratings");
            String service = extras.getString("service");
            List<StoreHours> storeHours = extras.getParcelableArrayList("storeHours");
            String imageUrl = extras.getString("imageURL");

            // 设置详细信息
            storeNameTxt.setText(storeName);
            categoryTxt.setText(category);
            addressTxt.setText(address);
            ratingsTxt.setText(String.valueOf(ratings));
            serviceTxt.setText(service);

            // 使用 Glide 加载图片
            Glide.with(this).load(imageUrl).into(storeImageView);

            // 设置营业时间信息
            StringBuilder hoursBuilder = new StringBuilder();
            if (storeHours != null) {
                for (StoreHours hours : storeHours) {
                    hoursBuilder.append(hours.getDayOfWeek())
                            .append(": ")
                            .append(hours.getOpenTime1())
                            .append(" - ")
                            .append(hours.getCloseTime1());
                    if (!hours.getOpenTime2().isEmpty() && !hours.getCloseTime2().isEmpty()) {
                        hoursBuilder.append(", ")
                                .append(hours.getOpenTime2())
                                .append(" - ")
                                .append(hours.getCloseTime2());
                    }
                    hoursBuilder.append("\n");
                }
            }
            hoursTxt.setText(hoursBuilder.toString());
        }

        // 設置點餐按鈕的點擊事件
        orderButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // 啟動新的 Activity 進行點餐
                Intent intent = new Intent(StoreDetailActivity.this, OrderActivity.class);
                startActivity(intent);
            }
        });

        // 設置返回按鈕的點擊事件
        backButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // 返回 FavorFragment
                finish();
            }
        });
    }
}
