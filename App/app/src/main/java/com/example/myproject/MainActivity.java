package com.example.myproject;

import android.os.Bundle;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

import android.os.Bundle;
import com.example.myproject.databinding.ActivityMainBinding;

public class MainActivity extends AppCompatActivity {
    ActivityMainBinding binding;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        // Check if there is a request to show a specific fragment
        String fragmentToShow = getIntent().getStringExtra("showFragment");
        if (fragmentToShow != null) {
            if (fragmentToShow.equals("FavorFragment")) {
                replaceFragment(new FavorFragment());
            }
        } else {
            // Default fragment
            replaceFragment(new AssistentFragment());
        }

        binding.bottomNavigationView.setOnItemSelectedListener(item -> {
            int itemId = item.getItemId();
            if (itemId == R.id.AssiSTent) {
                replaceFragment(new AssistentFragment());
                return true;
            } else if (itemId == R.id.FoodMap) {
                replaceFragment(new MapsFragment());
                return true;
            } else if (itemId == R.id.favor) {
                replaceFragment(new FavorFragment());
                return true;
            } else if (itemId == R.id.account) {
                replaceFragment(new AccountFragment());
                return true;
            } else {
                return super.onOptionsItemSelected(item);
            }
        });
    }

    void replaceFragment(Fragment fragment) {
        FragmentManager fragmentManager = getSupportFragmentManager();
        FragmentTransaction fragmentTransaction = fragmentManager.beginTransaction();
        fragmentTransaction.replace(R.id.frameLayout, fragment);
        fragmentTransaction.commit();
    }
}
