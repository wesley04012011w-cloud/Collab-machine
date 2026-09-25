package com.ollamastudio.mobile

import android.app.Activity
import android.os.Bundle
import android.graphics.Color
import android.view.Gravity
import android.widget.*
import org.json.JSONArray
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import kotlin.concurrent.thread

class MainActivity : Activity() {
    private lateinit var url: EditText
    private lateinit var model: EditText
    private lateinit var prompt: EditText
    private lateinit var output: TextView

    private fun request(path: String, method: String, body: String? = null): String {
        val base = url.text.toString().trim().removeSuffix("/")
        val c = URL(base + path).openConnection() as HttpURLConnection
        c.requestMethod = method
        c.connectTimeout = 8000
        c.readTimeout = 300000
        c.setRequestProperty("Content-Type", "application/json")
        if (body != null) {
            c.doOutput = true
            c.outputStream.use { it.write(body.toByteArray()) }
        }
        val text = (if (c.responseCode in 200..299) c.inputStream else c.errorStream).bufferedReader().use { it.readText() }
        if (c.responseCode !in 200..299) error(text)
        return text
    }

    private fun run(action: () -> String) {
        output.text = "⏳ trabalhando…"
        thread {
            try {
                val result = action()
                runOnUiThread { output.text = result }
            } catch (ex: Exception) {
                runOnUiThread { output.text = "❌ " + ex.message }
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(24, 28, 24, 24)
            setBackgroundColor(Color.rgb(11, 13, 18))
        }
        fun label(text: String) = TextView(this).apply {
            this.text = text; textSize = 13f; setTextColor(Color.LTGRAY); setPadding(0,12,0,5)
        }
        fun edit(hint: String, value: String = "") = EditText(this).apply {
            this.hint = hint; setText(value); setTextColor(Color.WHITE); setHintTextColor(Color.GRAY); setSingleLine(true)
        }
        fun button(text: String, action: () -> Unit) = Button(this).apply { this.text = text; setOnClickListener { action() } }

        root.addView(TextView(this).apply {
            text = "⚡ Ollama Studio"; textSize = 27f; setTextColor(Color.WHITE); gravity = Gravity.CENTER; setPadding(0,0,0,8)
        })
        root.addView(label("Servidor / Agent"))
        url = edit("https://seu-servidor/api/v1", "http://10.0.2.2:8000/api/v1")
        root.addView(url)
        val status = TextView(this).apply { setTextColor(Color.LTGRAY); text = "Pronto para conectar." }
        root.addView(status)
        root.addView(button("Conectar / testar") {
            run {
                val s = request("/status","GET")
                runOnUiThread { status.text = "✅ Backend respondeu" }
                s
            }
        })
        root.addView(label("Modelo"))
        model = edit("ex.: llama3.2:3b")
        root.addView(model)
        root.addView(button("Listar modelos") {
            run {
                val json = JSONObject(request("/ollama/models","GET"))
                val arr = json.optJSONArray("models") ?: JSONArray()
                val lines = mutableListOf<String>()
                for (i in 0 until arr.length()) lines += arr.getJSONObject(i).optString("name")
                if (lines.isEmpty()) "Nenhum modelo encontrado." else lines.joinToString("\n")
            }
        })
        root.addView(label("Mensagem"))
        prompt = edit("Digite sua mensagem")
        root.addView(prompt)
        root.addView(button("Enviar para Ollama") {
            run {
                val messages = JSONArray().put(JSONObject().put("role","user").put("content",prompt.text.toString()))
                val body = JSONObject().put("model",model.text.toString()).put("messages",messages).put("stream",false)
                val json = JSONObject(request("/ollama/chat","POST",body.toString()))
                json.optJSONObject("message")?.optString("content") ?: json.toString(2)
            }
        })
        output = TextView(this).apply { text = "Resposta aparecerá aqui."; textSize = 15f; setTextColor(Color.WHITE); setPadding(0,18,0,0) }
        root.addView(output)
        setContentView(ScrollView(this).apply { addView(root) })
    }
}