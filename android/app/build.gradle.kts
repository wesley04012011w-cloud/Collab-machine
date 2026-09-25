plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.ollamastudio.mobile"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.ollamastudio.mobile"
        minSdk = 26
        targetSdk = 35
        versionCode = 1
        versionName = "0.1.0"
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }

    signingConfigs {
        create("release") {
            val storeFilePath = System.getenv("ANDROID_KEYSTORE_PATH")
            val storePassword = System.getenv("ANDROID_KEYSTORE_PASSWORD")
            val keyAliasValue = System.getenv("ANDROID_KEY_ALIAS")
            val keyPasswordValue = System.getenv("ANDROID_KEY_PASSWORD")
            if (!storeFilePath.isNullOrBlank() && !storePassword.isNullOrBlank() &&
                !keyAliasValue.isNullOrBlank() && !keyPasswordValue.isNullOrBlank()) {
                storeFile = file(storeFilePath)
                this.storePassword = storePassword
                keyAlias = keyAliasValue
                keyPassword = keyPasswordValue
            }
        }
    }

    buildTypes {
        release {
            val hasSigning = System.getenv("ANDROID_KEYSTORE_PATH")?.isNotBlank() == true &&
                System.getenv("ANDROID_KEYSTORE_PASSWORD")?.isNotBlank() == true &&
                System.getenv("ANDROID_KEY_ALIAS")?.isNotBlank() == true &&
                System.getenv("ANDROID_KEY_PASSWORD")?.isNotBlank() == true
            if (hasSigning) signingConfig = signingConfigs.getByName("release")
            isMinifyEnabled = false
        }
        debug {
            applicationIdSuffix = ".debug"
            versionNameSuffix = "-debug"
        }
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.15.0")
    implementation("androidx.appcompat:appcompat:1.7.0")
}
