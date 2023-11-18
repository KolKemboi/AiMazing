package com.ombati.myapplication

import com.google.firebase.auth.FirebaseAuth
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.flowOn
import kotlinx.coroutines.tasks.await

class Authentication {
    private val auth = FirebaseAuth.getInstance()

    val isSignedIn: Boolean = auth.currentUser != null

    fun signUpUser(
        email: String,
        password: String,
    ): Flow<Result<Boolean>> = flow {
        try {
            auth.createUserWithEmailAndPassword(email, password).await()
            emit(Result.Success(true))
        } catch (e: Exception) {
            emit(Result.Error(e.message))
            e.printStackTrace()
        }
    }.flowOn(Dispatchers.IO)

    fun signInUser(
        email: String,
        password: String,
    ): Flow<Result<Boolean>> = flow {
        try {
            auth.signInWithEmailAndPassword(email, password).await()
            emit(Result.Success(true))
        } catch (e: Exception) {
            emit(Result.Error(e.message))
            e.printStackTrace()
        }
    }.flowOn(Dispatchers.IO)

    fun signOut(): Flow<Result<Boolean>> = flow {
        try {
            auth.signOut()
            emit(Result.Success(true))
        } catch (e: Exception) {
            emit(Result.Error(e.message))
        }
    }
}

sealed class Result<T>(val data: T? = null, val message: String? = null) {
    class Success<T>(data: T?) : Result<T>(data)
    class Error<T>(message: String?) : Result<T>(message = message)
}
