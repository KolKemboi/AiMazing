package com.ombati.myapplication

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.flowWithLifecycle
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.flow.launchIn
import kotlinx.coroutines.flow.onEach

class SignInActivity : AppCompatActivity() {
    private lateinit var authentication: Authentication
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_sign_in)
        authentication = Authentication()
        val email = findViewById<EditText>(R.id.et_login_email)
        val password = findViewById<EditText>(R.id.et_login_password)
        val signInButton = findViewById<Button>(R.id.btn_sign_in)


        signInButton.setOnClickListener {
            signIn(
                email = email.text.toString(),
                password = password.text.toString()
            )
        }
    }

    private fun signIn(
        email: String,
        password: String
    ) {
        if (email.isEmpty()) {
            Toast.makeText(this@SignInActivity, "Email cannot be empty", Toast.LENGTH_LONG).show()
            return
        }
        if (password.isEmpty()) {
            Toast.makeText(this@SignInActivity, "Password cannot be empty", Toast.LENGTH_LONG)
                .show()
            return
        }
        authentication.signInUser(email, password).onEach { result ->
            when (result) {
                is Result.Error -> {
                    Toast.makeText(this@SignInActivity, "Failed to log in", Toast.LENGTH_LONG)
                        .show()
                }

                is Result.Success -> {
                    val intent = Intent(this@SignInActivity, CameraActivity::class.java)
                    startActivity(intent)
                }
            }
        }.flowWithLifecycle(this.lifecycle, Lifecycle.State.RESUMED).launchIn(lifecycleScope)
    }
}