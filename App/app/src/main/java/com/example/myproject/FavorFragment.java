package com.example.myproject;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.android.volley.DefaultRetryPolicy;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.RetryPolicy;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.example.myproject.Adapter.FoodAdapter;
import com.example.myproject.Adapter.FoodItem;
import com.example.myproject.Adapter.StoreHours;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class FavorFragment extends Fragment {

    private RecyclerView recyclerView, recyclerView2, recyclerView3, recyclerView4,recyclerViewNew, recyclerViewCategory;
    private FoodAdapter foodAdapter, foodAdapter2, foodAdapter3, foodAdapter4, foodAdapterNew;
    private List<FoodItem> foodItems, foodItems2, foodItems3, foodItems4, foodItemsNew;
    private RequestQueue requestQueue;

    private Spinner categorySpinner;
    private ArrayAdapter<String> categorySpinnerAdapter;
    private List<String> categories;
    private ImageView cartButton;
    private ProgressBar progressBarForurFood, progressBarForurFood2, progressBarForurFood3, progressBarForurFood4, progressBarForurFoodNew, progressBarCategory;
    private LinearLayout linearLayoutHeader, linearLayoutYourFood, linearLayoutYourFood2, linearLayoutYourFood3, linearLayoutYourFood4, linearLayoutYourFoodNew, linearLayoutCategory;
    private TextView textView3, LastView, bestFoodView, categoryView, RecView;

    private EditText searchEditText;
    private ImageView searchButton;
    private boolean isDataFetched = false;

    public FavorFragment() {
        // Required empty public constructor
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_favor, container, false);

        // Initialize the list and adapter for the first section
        foodItems = new ArrayList<>();
        foodAdapter = new FoodAdapter(foodItems, getContext());

        // Initialize the list and adapter for the second section
        foodItems2 = new ArrayList<>();
        foodAdapter2 = new FoodAdapter(foodItems2, getContext());

        // Initialize the list and adapter for the basic recommendation (新推薦)
        foodItemsNew = new ArrayList<>();
        foodAdapterNew = new FoodAdapter(foodItemsNew, getContext());

        // Initialize the list and adapter for the third section
        foodItems3 = new ArrayList<>();
        foodAdapter3 = new FoodAdapter(foodItems3, getContext());

        // Initialize the list and adapter for the fourth section
        foodItems4 = new ArrayList<>();
        foodAdapter4 = new FoodAdapter(foodItems4, getContext());

        // Set up RecyclerView for the first section
        recyclerView = view.findViewById(R.id.YourFoodView);
        LinearLayoutManager layoutManager = new LinearLayoutManager(getContext(), LinearLayoutManager.HORIZONTAL, false);
        recyclerView.setLayoutManager(layoutManager);
        recyclerView.setAdapter(foodAdapter);

        // Set up RecyclerView for the basic recommendation
        recyclerViewNew = view.findViewById(R.id.YourFoodViewNew);
        LinearLayoutManager layoutManagerNew = new LinearLayoutManager(getContext(), LinearLayoutManager.HORIZONTAL, false);
        recyclerViewNew.setLayoutManager(layoutManagerNew);
        recyclerViewNew.setAdapter(foodAdapterNew);

        // Set up RecyclerView for the second section
        recyclerView2 = view.findViewById(R.id.YourFoodView2);
        LinearLayoutManager layoutManager2 = new LinearLayoutManager(getContext(), LinearLayoutManager.HORIZONTAL, false);
        recyclerView2.setLayoutManager(layoutManager2);
        recyclerView2.setAdapter(foodAdapter2);

        // Set up RecyclerView for the third section
        recyclerView3 = view.findViewById(R.id.YourFoodView3);
        LinearLayoutManager layoutManager3 = new LinearLayoutManager(getContext(), LinearLayoutManager.HORIZONTAL, false);
        recyclerView3.setLayoutManager(layoutManager3);
        recyclerView3.setAdapter(foodAdapter3);

        // Set up RecyclerView for the fourth section
        recyclerView4 = view.findViewById(R.id.YourFoodView4);
        LinearLayoutManager layoutManager4 = new LinearLayoutManager(getContext(), LinearLayoutManager.HORIZONTAL, false);
        recyclerView4.setLayoutManager(layoutManager4);
        recyclerView4.setAdapter(foodAdapter4);

        // Initialize the Spinner for categories
        categorySpinner = view.findViewById(R.id.CategorySP);
        categories = new ArrayList<>();
        categories.add("    "); // Add a default "Cancel Filter" option
        categorySpinnerAdapter = new ArrayAdapter<>(getContext(), android.R.layout.simple_spinner_item, categories);
        categorySpinnerAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        categorySpinner.setAdapter(categorySpinnerAdapter);

        // Find the views by their ID
        linearLayoutHeader = view.findViewById(R.id.linearLayoutHeader);
        linearLayoutYourFood = view.findViewById(R.id.linearLayoutYourFood);
        linearLayoutYourFoodNew = view.findViewById(R.id.linearLayoutYourFoodNew) ;
        linearLayoutYourFood2 = view.findViewById(R.id.linearLayoutYourFood2);
        linearLayoutYourFood3 = view.findViewById(R.id.linearLayoutYourFood3);
        linearLayoutYourFood4 = view.findViewById(R.id.linearLayoutYourFood4);
        linearLayoutCategory = view.findViewById(R.id.linearLayoutCategory);
        textView3 = view.findViewById(R.id.textView3);
        RecView = view.findViewById(R.id.RecView);
        LastView = view.findViewById(R.id.LastView);
        bestFoodView = view.findViewById(R.id.bestFoodView);
        categoryView = view.findViewById(R.id.categoryView);

        // Set up ProgressBar
        progressBarForurFood = view.findViewById(R.id.progressBarForurFood);
        progressBarForurFood2 = view.findViewById(R.id.progressBarForurFood2);
        progressBarForurFoodNew = view.findViewById(R.id.progressBarForurFoodNew) ;
        progressBarForurFood3 = view.findViewById(R.id.progressBarForurFood3);
        progressBarForurFood4 = view.findViewById(R.id.progressBarForurFood4);
        progressBarCategory = view.findViewById(R.id.ProgressBarCategory);

        // Set up Volley request queue
        requestQueue = Volley.newRequestQueue(getContext());

        // Fetch data from the server
        fetchCategoryData();
        fetchRecommendedData(); // Fetch recommended stores data

        // 確保數據只加載一次
        if (!isDataFetched) {
            fetchCategoryData();
            fetchRecommendedData();
            isDataFetched = true;
        } else {
            updateUIWithCachedData();
        }

        // Setup category spinner selection listener
        categorySpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                String selectedCategory = categories.get(position);
                if (selectedCategory.equals("    ")) {
                    // Show all sections if "取消篩選" is selected
                    linearLayoutHeader.setVisibility(View.GONE);
                    RecView.setVisibility(View.VISIBLE);
                    LastView.setVisibility(View.VISIBLE);
                    bestFoodView.setVisibility(View.VISIBLE);
                    categoryView.setVisibility(View.VISIBLE);
                    linearLayoutYourFood.setVisibility(View.GONE);
                    linearLayoutYourFood2.setVisibility(View.VISIBLE);
                    linearLayoutYourFoodNew.setVisibility(View.VISIBLE);
                    linearLayoutYourFood3.setVisibility(View.VISIBLE);
                    linearLayoutYourFood4.setVisibility(View.VISIBLE);
                    fetchFoodData();
                } else {
                    filterFoodItemsByCategory(selectedCategory);

                    // Hide the header and other layouts
                    linearLayoutHeader.setVisibility(View.VISIBLE);
                    RecView.setVisibility(View.GONE);
                    LastView.setVisibility(View.GONE);
                    bestFoodView.setVisibility(View.GONE);
                    categoryView.setVisibility(View.GONE);
                    linearLayoutYourFood.setVisibility(View.VISIBLE);
                    linearLayoutYourFood2.setVisibility(View.GONE);
                    linearLayoutYourFoodNew.setVisibility(View.GONE);
                    linearLayoutYourFood3.setVisibility(View.GONE);
                    linearLayoutYourFood4.setVisibility(View.GONE);
                    linearLayoutCategory.setVisibility(View.VISIBLE);
                }
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {
                // Do nothing
            }
        });

        // Setup cart button click listener
        cartButton = view.findViewById(R.id.cartbtn);
        cartButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Start CartActivity when cart button is clicked
                Intent intent = new Intent(getContext(), CartActivity.class);
                startActivity(intent);
            }
        });

        searchEditText = view.findViewById(R.id.editTextText);
        searchButton = view.findViewById(R.id.search);
        // Set up search button click listener
        searchButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String query = searchEditText.getText().toString().trim();
                if (!query.isEmpty()) {
                    Intent intent = new Intent(getContext(), SearchResultActivity.class);
                    intent.putExtra("query", query);
                    startActivity(intent);
                } else {
                    Toast.makeText(getContext(), "請輸入搜索詞", Toast.LENGTH_SHORT).show();
                }
            }
        });

        return view;
    }

    private void fetchRecommendedData() {
        SharedPreferences sharedPreferences = getActivity().getSharedPreferences("MyPrefs", getContext().MODE_PRIVATE);
        String clientId = sharedPreferences.getString("id", null);

        if (clientId == null) {
            Toast.makeText(getContext(), "未能獲取用戶ID", Toast.LENGTH_SHORT).show();
            return;
        }
        String url = "https://subdomain2.jp.ngrok.io/recommend2";  // 更新為正確的 URL

        progressBarForurFood2.setVisibility(View.VISIBLE);
        progressBarForurFoodNew.setVisibility(View.VISIBLE);  // 顯示基本模式的進度條

        Map<String, String> params = new HashMap<>();
        params.put("client_id", clientId);

        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(
                Request.Method.POST,
                url,
                new JSONObject(params),
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        progressBarForurFood2.setVisibility(View.GONE);
                        progressBarForurFoodNew.setVisibility(View.GONE);
                        try {
                            // 打印整個響應 JSON 以確認結構
                            Log.d("FavorFragment", "Response JSON: " + response.toString());
                            foodItems2.clear();
                            foodItemsNew.clear();

                            // 檢查是否包含 recommendations_basic 和 recommendations_distance
                            if (response.has("recommendations_basic") && response.has("recommendations_distance")) {
                                // 基本模式推薦解析
                                JSONArray basicArray = response.getJSONArray("recommendations_basic");
                                for (int i = 0; i < basicArray.length(); i++) {
                                    JSONObject jsonObject = basicArray.getJSONObject(i);
                                    try {
                                        // 確保 JSON 包含所有必要字段
                                        String storeName = jsonObject.optString("store_name", "");
                                        String category = jsonObject.optString("category", "");
                                        String address = jsonObject.optString("address", "");
                                        float ratings = (float) jsonObject.optDouble("ratings", 0.0);
                                        String service = jsonObject.optString("service", "");

                                        // 解析營業時間
                                        JSONArray storeHoursArray = jsonObject.optJSONArray("store_hours");
                                        List<StoreHours> storeHoursList = new ArrayList<>();
                                        if (storeHoursArray != null) {
                                            for (int j = 0; j < storeHoursArray.length(); j++) {
                                                JSONObject hoursObject = storeHoursArray.getJSONObject(j);
                                                String dayOfWeek = hoursObject.optString("day_of_week", "");
                                                String openTime1 = hoursObject.optString("open_time_1", "");
                                                String closeTime1 = hoursObject.optString("close_time_1", "");
                                                String openTime2 = hoursObject.optString("open_time_2", "");
                                                String closeTime2 = hoursObject.optString("close_time_2", "");

                                                storeHoursList.add(new StoreHours(dayOfWeek, openTime1, closeTime1, openTime2, closeTime2));
                                            }
                                        }

                                        String imageUrl = jsonObject.optString("url", "");

                                        FoodItem foodItem = new FoodItem(storeName, category, address, ratings, service, storeHoursList, imageUrl);
                                        foodItemsNew.add(foodItem);
                                    } catch (JSONException e) {
                                        Log.e("FavorFragment", "Error parsing basic recommendation: " + e.getMessage());
                                    }
                                }
                                foodAdapterNew.notifyDataSetChanged();

                                // 距離過濾2模式推薦解析
                                JSONArray distanceArray = response.getJSONArray("recommendations_distance");
                                for (int i = 0; i < distanceArray.length(); i++) {
                                    JSONObject jsonObject = distanceArray.getJSONObject(i);
                                    try {
                                        String storeName = jsonObject.optString("store_name", "");
                                        String category = jsonObject.optString("category", "");
                                        String address = jsonObject.optString("address", "");
                                        float ratings = (float) jsonObject.optDouble("ratings", 0.0);
                                        String service = jsonObject.optString("service", "");

                                        JSONArray storeHoursArray = jsonObject.optJSONArray("store_hours");
                                        List<StoreHours> storeHoursList = new ArrayList<>();
                                        if (storeHoursArray != null) {
                                            for (int j = 0; j < storeHoursArray.length(); j++) {
                                                JSONObject hoursObject = storeHoursArray.getJSONObject(j);
                                                String dayOfWeek = hoursObject.optString("day_of_week", "");
                                                String openTime1 = hoursObject.optString("open_time_1", "");
                                                String closeTime1 = hoursObject.optString("close_time_1", "");
                                                String openTime2 = hoursObject.optString("open_time_2", "");
                                                String closeTime2 = hoursObject.optString("close_time_2", "");

                                                storeHoursList.add(new StoreHours(dayOfWeek, openTime1, closeTime1, openTime2, closeTime2));
                                            }
                                        }

                                        String imageUrl = jsonObject.optString("url", "");

                                        FoodItem foodItem = new FoodItem(storeName, category, address, ratings, service, storeHoursList, imageUrl);
                                        foodItems2.add(foodItem);
                                    } catch (JSONException e) {
                                        Log.e("FavorFragment", "Error parsing distance recommendation: " + e.getMessage());
                                    }
                                }
                                foodAdapter2.notifyDataSetChanged();
                            } else {
                                Log.e("FavorFragment", "JSON missing expected arrays: recommendations_basic or recommendations_distance");
                                Toast.makeText(getContext(), "Unexpected JSON structure", Toast.LENGTH_SHORT).show();
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                            Toast.makeText(getContext(), "Failed to parse JSON data", Toast.LENGTH_SHORT).show();
                        }
                    }

                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        progressBarForurFood2.setVisibility(View.GONE);
                        progressBarForurFoodNew.setVisibility(View.GONE);  // 隱藏基本模式的進度條
                        error.printStackTrace();
                        Toast.makeText(getContext(), "Failed to fetch data", Toast.LENGTH_SHORT).show();
                    }
                });

        int socketTimeout = 30000; // 30 seconds
        RetryPolicy policy = new DefaultRetryPolicy(socketTimeout,
                DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                DefaultRetryPolicy.DEFAULT_BACKOFF_MULT);

        jsonObjectRequest.setRetryPolicy(policy);
        requestQueue.add(jsonObjectRequest);
    }




    private void fetchFoodData() {
        String url = "https://subdomain1.jp.ngrok.io/login-register-android/fetch_food_data.php";

        progressBarForurFood.setVisibility(View.VISIBLE);
        progressBarForurFood3.setVisibility(View.VISIBLE);
        progressBarForurFood4.setVisibility(View.VISIBLE);

        JsonArrayRequest jsonArrayRequest = new JsonArrayRequest(
                Request.Method.GET,
                url,
                null,
                new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {
                        progressBarForurFood.setVisibility(View.GONE);
                        progressBarForurFood3.setVisibility(View.GONE);
                        progressBarForurFood4.setVisibility(View.GONE);
                        try {
                            Log.d("FavorFragment", "Response: " + response.toString());
                            foodItems.clear();
                            foodItems3.clear();
                            foodItems4.clear();
                            for (int i = 0; i < response.length(); i++) {
                                JSONObject jsonObject = response.getJSONObject(i);

                                String storeName = jsonObject.getString("store_name");
                                String category = jsonObject.getString("category");
                                String address = jsonObject.getString("address");
                                float ratings = (float) jsonObject.getDouble("ratings");
                                String service = jsonObject.getString("service");

                                // 解析營業時間
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

                                // Add the same food item to all three lists
                                foodItems.add(foodItem);
                                foodItems3.add(foodItem);
                                foodItems4.add(foodItem);
                            }

                            foodAdapter.notifyDataSetChanged();
                            foodAdapter3.notifyDataSetChanged();
                            foodAdapter4.notifyDataSetChanged();
                        } catch (JSONException e) {
                            e.printStackTrace();
                            Toast.makeText(getContext(), "Failed to parse JSON data", Toast.LENGTH_SHORT).show();
                        }
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        progressBarForurFood.setVisibility(View.GONE);
                        progressBarForurFood3.setVisibility(View.GONE);
                        progressBarForurFood4.setVisibility(View.GONE);
                        error.printStackTrace();
                        Toast.makeText(getContext(), "Failed to fetch data", Toast.LENGTH_SHORT).show();
                    }
                });


        requestQueue.add(jsonArrayRequest);
    }

    private void fetchCategoryData() {
        String url = "https://localhost/login-register-android/fetch_category_data.php";

        progressBarCategory.setVisibility(View.VISIBLE);

        JsonArrayRequest jsonArrayRequest = new JsonArrayRequest(
                Request.Method.GET,
                url,
                null,
                new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {
                        progressBarCategory.setVisibility(View.GONE);
                        try {
                            Log.d("FavorFragment", "Category Response: " + response.toString());
                            categories.clear();
                            categories.add("    "); // Add a default "Cancel Filter" option
                            for (int i = 0; i < response.length(); i++) {
                                JSONObject jsonObject = response.getJSONObject(i);
                                String category = jsonObject.getString("category");
                                categories.add(category);
                            }

                            categorySpinnerAdapter.notifyDataSetChanged();
                        } catch (JSONException e) {
                            e.printStackTrace();
                            Toast.makeText(getContext(), "Failed to parse JSON data", Toast.LENGTH_SHORT).show();
                        }
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        progressBarCategory.setVisibility(View.GONE);
                        error.printStackTrace();
                        Toast.makeText(getContext(), "Failed to fetch data", Toast.LENGTH_SHORT).show();
                    }
                });

        requestQueue.add(jsonArrayRequest);
    }

    private void filterFoodItemsByCategory(String category) {
        List<FoodItem> filteredFoodItems = new ArrayList<>(); // 創一個新list，保存所有符合篩選條件的店家。
        for (FoodItem item : foodItems) { //遍壢foodItems，檢查每個FoodItem是否符合所選的類別。
            if (item.getCategory().equals(category)) {  //把符合條件的FoodItem添加到filteredFoodItems
                filteredFoodItems.add(item);
            }
        }

        // 更新 RecyclerViewAdapter
        foodAdapter = new FoodAdapter(filteredFoodItems, getContext());
        recyclerView.setAdapter(foodAdapter);
        foodAdapter.notifyDataSetChanged();
    }

    private void updateUIWithCachedData() {
        foodAdapterNew.notifyDataSetChanged();
        foodAdapter2.notifyDataSetChanged();
    }
}
