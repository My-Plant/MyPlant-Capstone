package com.example.kepston

import android.content.Intent
import android.graphics.Color
import android.graphics.drawable.ColorDrawable
import android.os.Bundle
import android.view.WindowManager
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.isVisible
import androidx.recyclerview.widget.GridLayoutManager
import com.example.kepston.api.ApiConfig1
import com.example.kepston.databinding.ActivityDaftarPenyakitBinding
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.onCompletion
import kotlinx.coroutines.flow.onStart
import kotlinx.coroutines.launch

class DaftarPenyakitActivity : AppCompatActivity() {

    private lateinit var binding: ActivityDaftarPenyakitBinding
    private val adapter by lazy {
        PenyakitAdapter {
            Intent(this, DetailPenyakitActivity::class.java).apply {
                putExtra("id", it.id)
                putExtra("nama2", it.nama)
                putExtra("deskripsi2", it.deskripsi.joinToString(separator = " "))
                putExtra("solusi2", it.solusi.joinToString(separator = " "))
                putExtra("foto2", it.foto)
                startActivity(this)
            }
        }
    }
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.setFlags(
            WindowManager.LayoutParams.FLAG_FULLSCREEN,
            WindowManager.LayoutParams.FLAG_FULLSCREEN
        )
        binding = ActivityDaftarPenyakitBinding.inflate(layoutInflater)
        setContentView(binding.root)

        supportActionBar!!.setBackgroundDrawable(ColorDrawable(Color.parseColor("#B0BD9A")))

        binding.recyclerView.setHasFixedSize(true)
        binding.recyclerView.adapter = adapter

        binding.recyclerView.layoutManager = GridLayoutManager(this, 2)

        val actionBar = supportActionBar
        actionBar?.setElevation(0F);
        actionBar?.setDisplayHomeAsUpEnabled(true)
        actionBar?.setDisplayHomeAsUpEnabled(true)

        GlobalScope.launch(Dispatchers.IO) {
            launch (Dispatchers.Main){
                flow {
                    val response = ApiConfig1
                        .apiService
                        .getPenyakit()

                    emit(response)
                }.onStart {
                    binding.progressBar.isVisible = true
                }.onCompletion {
                    binding.progressBar.isVisible = false
                }.catch {
                    Toast.makeText(
                        this@DaftarPenyakitActivity, it.message.toString(),
                        Toast.LENGTH_SHORT
                    ).show()
                }.collect{
                    adapter.setData(it)
                }
            }
        }
    }

    override fun onSupportNavigateUp(): Boolean {
        onBackPressed()
        return true
    }
}