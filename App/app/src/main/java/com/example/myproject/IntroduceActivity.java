package com.example.myproject;


import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;
import androidx.viewpager2.widget.ViewPager2;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;

import com.example.myproject.Adapter.OnboardingItem;
import com.google.android.material.button.MaterialButton;

import java.util.ArrayList;
import java.util.List;

public class IntroduceActivity extends AppCompatActivity {

    private com.example.myproject.Adapter.OnboardingAdapter onboardingAdapter ;
    private LinearLayout layoutOnboardingIndicators ;

    private MaterialButton buttonOnboardingAction ;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_introduce);

        layoutOnboardingIndicators = findViewById(R.id.LayoutOnboardingIndicators) ;
        buttonOnboardingAction = findViewById(R.id.buttonOnboardingAction) ;

        setupOnboardingItems();

        ViewPager2 onboardingViewPager = findViewById(R.id.onboardingViewPager) ;
        onboardingViewPager.setAdapter(onboardingAdapter);

        setupOnboardingIndicators();
        setCurrentOnboardingIndicators(0) ;

        onboardingViewPager.registerOnPageChangeCallback(new ViewPager2.OnPageChangeCallback() {
            @Override
            public void onPageSelected(int position) {
                super.onPageSelected(position);
                setCurrentOnboardingIndicators(position);
            }
        });

        buttonOnboardingAction.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(onboardingViewPager.getCurrentItem() < onboardingAdapter.getItemCount() - 1 ){
                    onboardingViewPager.setCurrentItem(onboardingViewPager.getCurrentItem() + 1 );

                } // if
                else{
                    startActivity(new Intent(getApplicationContext(), InterestSelectActivity.class));
                    finish();
                } // else
            }
        });
    }

    private void setupOnboardingItems(){
        List<OnboardingItem> onboardingItems = new ArrayList<>();

        OnboardingItem Greeting = new OnboardingItem();
        Greeting.setTitle("哈囉:D歡迎來到訂食吧");
        Greeting.setDescription("歡迎來到訂時吧");
        Greeting.setAnimationRes(R.raw.greet); // 使用 Lottie 動畫

        OnboardingItem MeetManager = new OnboardingItem();
        MeetManager.setTitle("不知道要吃什麼?那就來使用語音助理吧!");
        MeetManager.setDescription("那就來使用語音助理吧!");
        MeetManager.setAnimationRes(R.raw.chatbot); // 使用 Lottie 動畫

        OnboardingItem GetStarted = new OnboardingItem();
        GetStarted.setTitle("準備好來使用了?快按右下角準備吃大餐囉!");
        GetStarted.setDescription("快按右下角開始訂餐來大吃大喝!");
        GetStarted.setAnimationRes(R.raw.lastt); // 使用 Lottie 動畫

        onboardingItems.add(Greeting);
        onboardingItems.add(MeetManager);
        onboardingItems.add(GetStarted);

        onboardingAdapter = new com.example.myproject.Adapter.OnboardingAdapter(onboardingItems);
    }

    private void setupOnboardingIndicators(){
        ImageView[] indicators = new ImageView[onboardingAdapter.getItemCount()] ;
        LinearLayout.LayoutParams layoutParams = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT
        );
        layoutParams.setMargins(8,0,8,0) ;
        for ( int i = 0 ; i < indicators.length ; i++ ){
            indicators[i] = new ImageView(getApplicationContext());
            indicators[i].setImageDrawable(ContextCompat.getDrawable(
                    getApplicationContext(),R.drawable.onboarding_indicator_inactive
            ));
            indicators[i].setLayoutParams(layoutParams);
            layoutOnboardingIndicators.addView(indicators[i]) ;
        }
    }

    private void setCurrentOnboardingIndicators( int index ){
        int childCount = layoutOnboardingIndicators.getChildCount() ;
        for ( int i = 0 ; i < childCount ; i++ ){
            ImageView imageView = (ImageView) layoutOnboardingIndicators.getChildAt(i);
            if( i == index ){
                imageView.setImageDrawable(
                        ContextCompat.getDrawable(getApplicationContext(),R.drawable.onboarding_indicator_active)
                );
            } // if
            else{
                imageView.setImageDrawable(
                        ContextCompat.getDrawable(getApplicationContext(),R.drawable.onboarding_indicator_inactive)
                );
            } // else
        } // for

        if (index == onboardingAdapter.getItemCount() - 1 )
            buttonOnboardingAction.setText("開始") ;
        else
            buttonOnboardingAction.setText("下一個");
    } // void
}