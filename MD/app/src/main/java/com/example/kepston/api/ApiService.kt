package com.example.kepston.api

import com.google.gson.annotations.SerializedName
import okhttp3.MultipartBody
import okhttp3.OkHttpClient
import okhttp3.RequestBody
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Call
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.create
import retrofit2.http.*
import kotlin.collections.ArrayList

data class FileUploadResponse(
    @field:SerializedName("image_url")
    val image_url: String,

    @field:SerializedName("prediction")
    val prediction: String,

    @field:SerializedName("deskripsi")
    val deskripsi: ArrayList<String>,

    @field:SerializedName("solusi")
    val solusi: ArrayList<String>
)

//data class PenyakitResponse(
//
//    @field:SerializedName("foto")
//    val foto: String,
//
//    @field:SerializedName("id")
//    val id: Int,
//
//    @field:SerializedName("repos_url")
//    val nama: String,
//)

data class PenyakitResponse(

    @field:SerializedName("PenyakitResponse")
    val penyakitResponse: MutableList<PenyakitResponseItem>
) {
    data class PenyakitResponseItem(

        @field:SerializedName("foto")
        val foto: String,

        @field:SerializedName("nama")
        val nama: String,

        @field:SerializedName("solusi")
        val solusi: List<String>,

        @field:SerializedName("deskripsi")
        val deskripsi: List<String>,

        @field:SerializedName("id")
        val id: String
    )
}

data class DetailPenyakitResponse(

    @field:SerializedName("deskripsi")
    val deskripsi: ArrayList<String>,

    @field:SerializedName("foto")
    val foto: String,

    @field:SerializedName("nama")
    val nama: String,

    @field:SerializedName("id")
    val id: String,

    @field:SerializedName("solusi")
    val solusi: ArrayList<String>
)

interface ApiService {
    @Multipart
    @POST("/predict")
    fun uploadImage(
        @Part file: MultipartBody.Part,
    ): Call<FileUploadResponse>

    @JvmSuppressWildcards
    @GET("penyakit")
    suspend fun getPenyakit(): MutableList<PenyakitResponse.PenyakitResponseItem>

    @JvmSuppressWildcards
    @GET("penyakit/{id")
    suspend fun getDetailPenyakit(@Path("id") id: String): DetailPenyakitResponse

//    @GET("/penyakit/{id}")
//    fun getDetailPenyakit(@Path("id") id: String): DetailPenyakitResponse
}

class ApiConfig {
    fun getApiService(): ApiService {
        val loggingInterceptor =
            HttpLoggingInterceptor().setLevel(HttpLoggingInterceptor.Level.BODY)
        val client = OkHttpClient.Builder()
            .addInterceptor(loggingInterceptor)
            .build()
        val retrofit = Retrofit.Builder()
            .baseUrl("https://project-firebase-387302.et.r.appspot.com/")
            .addConverterFactory(GsonConverterFactory.create())
            .client(client)
            .build()
        return retrofit.create(ApiService::class.java)
    }
}

object ApiConfig1 {
    private val client = OkHttpClient.Builder()
        .apply {
            val loggingInterceptor = HttpLoggingInterceptor()
            loggingInterceptor.level = HttpLoggingInterceptor.Level.BODY
            addInterceptor(loggingInterceptor)
        }
        .build()

    private val BASE_URL = "https://project-firebase-387302.et.r.appspot.com/"

    private val retrofit = Retrofit.Builder()
        .baseUrl(BASE_URL)
        .client(client)
        .addConverterFactory(GsonConverterFactory.create())
        .build()

    val apiService = retrofit.create<ApiService>()
}