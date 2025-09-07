package com.example.myproject;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ImageButton;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.Volley;
import com.example.myproject.Adapter.CartAdapter;
import com.example.myproject.Adapter.CartItem;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

public class CartActivity extends AppCompatActivity {

    private RecyclerView recyclerViewCart;
    private CartAdapter cartAdapter;
    private List<CartItem> cartItemList;
    private TextView totalPriceTxt;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_cart);

        // Initialize views
        recyclerViewCart = findViewById(R.id.recyclerViewCart);
        totalPriceTxt = findViewById(R.id.totalPrice);
        ImageButton backButton = findViewById(R.id.backButton);

        // Set up back button
        backButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });

        // Initialize cart item list and adapter
        cartItemList = new ArrayList<>();
        cartAdapter = new CartAdapter(cartItemList, this);
        recyclerViewCart.setLayoutManager(new LinearLayoutManager(this));
        recyclerViewCart.setAdapter(cartAdapter);

        // Fetch cart items from server
        fetchCartItems();
    }

    private void fetchCartItems() {
        SharedPreferences sharedPreferences = getSharedPreferences("MyPrefs", MODE_PRIVATE);
        String userId = sharedPreferences.getString("id", null);
        if (userId == null) {
            // Handle case where user is not logged in
            return;
        }

        String url = apiURLs.GET_CART_ITEMS + userId;
        JsonArrayRequest jsonArrayRequest = new JsonArrayRequest(Request.Method.GET, url, null,
                new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {
                        cartItemList.clear();
                        double totalPrice = 0.0;
                        try {
                            for (int i = 0; i < response.length(); i++) {
                                JSONObject jsonObject = response.getJSONObject(i);
                                String productName = jsonObject.getString("product_name");
                                int quantity = jsonObject.getInt("quantity");
                                double price = jsonObject.getDouble("price");
                                CartItem cartItem = new CartItem(productName, quantity, price);
                                cartItemList.add(cartItem);
                                totalPrice += price * quantity;
                            }
                            cartAdapter.notifyDataSetChanged();
                            totalPriceTxt.setText("$" + String.format("%.2f", totalPrice));
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Log.e("CartActivity", "Error fetching cart items", error);
            }
        });

        RequestQueue requestQueue = Volley.newRequestQueue(this);
        requestQueue.add(jsonArrayRequest);
    }
}
