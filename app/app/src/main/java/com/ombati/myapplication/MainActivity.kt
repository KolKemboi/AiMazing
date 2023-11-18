package com.ombati.myapplication

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.flowWithLifecycle
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.flow.launchIn
import kotlinx.coroutines.flow.onEach

class MainActivity : AppCompatActivity() {
    private lateinit var authentication: Authentication
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        authentication = Authentication()
        val email: EditText = findViewById(R.id.et_email)
        val password: EditText = findViewById(R.id.et_password)
        val signUpButton: Button = findViewById(R.id.btn_sign_up)
        val confirmPassword: EditText = findViewById(R.id.et_confirm_password)
        val loginButton: TextView = findViewById(R.id.tv_login)


        if (authentication.isSignedIn) {
            navigateToCamera()
        }
        loginButton.setOnClickListener {
            val intent = Intent(this@MainActivity, SignInActivity::class.java)
            startActivity(intent)
        }

        signUpButton.setOnClickListener {
            signUpUser(
                email = email.text.toString(),
                password = password.text.toString(),
                confirmPassword = confirmPassword.text.toString(),
            )
        }
    }

    private fun signUpUser(
        email: String,
        password: String,
        confirmPassword: String,
    ) {
        if (email.isEmpty()) {
            Toast.makeText(this@MainActivity, "Email cannot be empty", Toast.LENGTH_LONG).show()
            return
        }
        if (password.isEmpty()) {
            Toast.makeText(this@MainActivity, "Password cannot be empty", Toast.LENGTH_LONG).show()
            return
        }
        if (password != confirmPassword) {
            Toast.makeText(
                this@MainActivity,
                "Password and confirm password do not match",
                Toast.LENGTH_LONG,
            ).show()
            return
        }
        authentication.signUpUser(email, password).onEach { result ->
            when (result) {
                is Result.Error -> {
                    Toast.makeText(this@MainActivity, "Failed to register", Toast.LENGTH_LONG)
                        .show()
                }

                is Result.Success -> {
                    navigateToCamera()
                }
            }
        }.flowWithLifecycle(this.lifecycle, Lifecycle.State.RESUMED).launchIn(lifecycleScope)
    }

    private fun navigateToCamera() {
        val intent = Intent(this@MainActivity, CameraActivity::class.java)
        startActivity(intent)
        finish()
    }
}
