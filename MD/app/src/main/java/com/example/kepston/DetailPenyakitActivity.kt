package com.example.kepston

import android.content.res.ColorStateList
import android.graphics.Color
import android.graphics.drawable.ColorDrawable
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.WindowManager
import androidx.annotation.ColorRes
import androidx.core.content.ContextCompat
import com.bumptech.glide.Glide
import com.bumptech.glide.request.RequestOptions
import com.example.kepston.databinding.ActivityDetailPenyakitBinding
import com.google.android.material.floatingactionbutton.FloatingActionButton

class DetailPenyakitActivity : AppCompatActivity() {

    private lateinit var binding: ActivityDetailPenyakitBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.setFlags(
            WindowManager.LayoutParams.FLAG_FULLSCREEN,
            WindowManager.LayoutParams.FLAG_FULLSCREEN
        )
        binding = ActivityDetailPenyakitBinding.inflate(layoutInflater)
        val view = binding.root
        setContentView(view)

        supportActionBar!!.setBackgroundDrawable(ColorDrawable(Color.parseColor("#B0BD9A")))

        val nama = intent.getStringExtra("nama2")
        val foto = intent.getStringExtra("foto2")
        val deskripsi = intent.getStringExtra("deskripsi2")
        val solusi = intent.getStringExtra("solusi2")

        val requestOptions = RequestOptions()
            .placeholder(R.drawable.progress_animation)
            .error(R.drawable.ic_error)

        Glide.with(this)
            .load(foto)
            .apply(requestOptions)
            .into(binding.daun)

        binding.jenis.text = nama
        binding.penjelasan.text = deskripsi
        binding.solusilengkap.text = solusi

        val actionBar = supportActionBar
        actionBar?.setElevation(0F);
        actionBar?.setDisplayHomeAsUpEnabled(true)
        actionBar?.setDisplayHomeAsUpEnabled(true)

        binding.fabLike.setOnClickListener {
            binding.fabLike.changeIconColor(R.color.black)
        }
        binding.fabDislike.setOnClickListener {
            binding.fabDislike.changeIconColor(R.color.black)
        }
    }

    override fun onSupportNavigateUp(): Boolean {
        onBackPressed()
        return true
    }

    fun FloatingActionButton.changeIconColor(@ColorRes color: Int){
        imageTintList = ColorStateList.valueOf(ContextCompat.getColor(this.context, color))
    }
}