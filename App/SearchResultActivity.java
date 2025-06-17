package com.example.myproject;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.android.volley.DefaultRetryPolicy;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.Volley;
import com.example.myproject.Adapter.FoodAdapter;
import com.example.myproject.Adapter.FoodItem;
import com.example.myproject.Adapter.StoreHours;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

public class SearchResultActivity extends AppCompatActivity {

    private EditText searchEditText;
    private ImageView searchButton;
    private RecyclerView searchResultsRecyclerView;
    private FoodAdapter foodAdapter;
    private List<FoodItem> foodItems;
    private RequestQueue requestQueue;
    private ProgressBar progressBar;

    private ImageView backButton;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_search_result);

        searchEditText = findViewById(R.id.searchEditText);
        searchButton = findViewById(R.id.searchButton);
        searchResultsRecyclerView = findViewById(R.id.searchResultsRecyclerView);
        backButton = findViewById(R.id.backButton);
        progressBar = findViewById(R.id.progressBar);

        foodItems = new ArrayList<>();
        foodAdapter = new FoodAdapter(foodItems, this);

        searchResultsRecyclerView.setLayoutManager(new LinearLayoutManager(this));
        searchResultsRecyclerView.setAdapter(foodAdapter);

        // 測試數據
        FoodItem testItem = new FoodItem("Test Store", "Category", "Address", 4.5f, "Service", new ArrayList<>(), "https://example.com/image.jpg");
        foodItems.add(testItem);
        foodAdapter.notifyDataSetChanged();

        requestQueue = Volley.newRequestQueue(this);

        // 獲取 Intent 中的查詢字串
        Intent intent = getIntent();
        String query = intent.getStringExtra("query");

        // 設置查詢字串到搜索欄
        searchEditText.setText(query);

        // 獲取搜索結果
        fetchSearchResults(query);

        // 設置搜索按鈕的點擊監聽器
        searchButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String newQuery = searchEditText.getText().toString().trim();
                if (!newQuery.isEmpty()) {
                    fetchSearchResults(newQuery);
                } else {
                    Toast.makeText(SearchResultActivity.this, "請輸入搜索詞", Toast.LENGTH_SHORT).show();
                }
            }
        });

        // 設置返回按鈕的點擊監聽器
        backButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(SearchResultActivity.this, MainActivity.class);
                intent.putExtra("showFragment", "FavorFragment");
                startActivity(intent);
                finish();
            }
        });
    }

    private void fetchSearchResults(String query) {
        String url = "https://subdomain1.jp.ngrok.io/login-register-android/fetch_search_results.php?query=" + query;

        progressBar.setVisibility(View.VISIBLE);

        JsonArrayRequest jsonArrayRequest = new JsonArrayRequest(
                Request.Method.GET,
                url,
                null,
                new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {
                        progressBar.setVisibility(View.GONE);
                        try {
                            Log.d("SearchResult", "Response: " + response.toString());
                            foodItems.clear();
                            for (int i = 0; i < response.length(); i++) {
                                JSONObject jsonObject = response.getJSONObject(i);

                                String storeName = jsonObject.getString("store_name");
                                String category = jsonObject.getString("category");
                                String address = jsonObject.getString("address");
                                float ratings = (float) jsonObject.getDouble("ratings");
                                String service = jsonObject.getString("service");

                                JSONArray storeHoursArray = jsonObject.getJSONArray("store_hours");
                                List<StoreHours> storeHoursList = new ArrayList<>();
                                for (int j = 0; j < storeHoursArray.length(); j++) {
                                    JSONObject hoursObject = storeHoursArray.getJSONObject(j);
                                    String dayOfWeek = hoursObject.getString("day_of_week");
                                    String openTime1 = hoursObject.getString("open_time_1");
                                    String closeTime1 = hoursObject.getString("close_time_1");
                                    String openTime2 = hoursObject.getString("open_time_2");
                                    String closeTime2 = hoursObject.getString("close_time_2");

                                    storeHoursList.add(new StoreHours(dayOfWeek, openTime1, closeTime1, openTime2, closeTime2));
                                }

                                String imageURL = jsonObject.getString("store_url");
                                FoodItem foodItem = new FoodItem(storeName, category, address, ratings, service, storeHoursList, imageURL);

                                foodItems.add(foodItem);
                            }

                            foodAdapter.notifyDataSetChanged();
                        } catch (JSONException e) {
                            e.printStackTrace();
                            Log.e("SearchResult", "JSON parsing error: " + e.getMessage());
                            Toast.makeText(SearchResultActivity.this, "Failed to parse JSON data", Toast.LENGTH_SHORT).show();
                        }
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        progressBar.setVisibility(View.GONE);
                        Log.e("SearchResult", "Volley error: " + error.getMessage(), error);
                        Toast.makeText(SearchResultActivity.this, "Failed to fetch data: " + error.getMessage(), Toast.LENGTH_SHORT).show();
                    }
                });

        // Set retry policy in case of SocketTimeout & ConnectionTimeout Exceptions. Volley does retry for you if you have specified the policy.
        jsonArrayRequest.setRetryPolicy(new DefaultRetryPolicy(
                10000, // Timeout in milliseconds
                DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));

        requestQueue.add(jsonArrayRequest);
    }
}
