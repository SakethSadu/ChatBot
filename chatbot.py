'''
 * @FileName: chatbot.py
 * @Project: ChatBot Application
 * @Author: Saketh Sadu
 * @Date: 12/23/2024 17:10:47
 * @LastEditTime:  04/18/2025 10:30:27
 * @Description: Implementation of a simple HTTP server that serves a chatbot interface and handles chat requests.
 '''

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import openai

api_key = "your_api_key_here"

class ChatBotHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("home.html", "rb") as file:
                self.wfile.write(file.read())
        elif self.path == "/style.css":
            self.send_response(200)
            self.send_header("Content-type", "text/css")
            self.end_headers()
            with open("style.css", "rb") as file:
                self.wfile.write(file.read())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/chatbot/":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            user_message = data.get("message", "")
            if not user_message:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"reply": "❗ Please enter a message."}).encode())
                return

            try:
                with open("System_Prompt.txt", "r") as file:
                    chatbot_prompt = file.read()
            except Exception as e:
                chatbot_prompt = "Default prompt: Unable to load system prompt."

            try:
                openai.api_key = api_key
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": chatbot_prompt},
                        {"role": "user", "content": user_message},
                    ],
                )
                reply = response["choices"][0]["message"]["content"]
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"reply": reply}).encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"reply": f"❗ OpenAI error: {str(e)}"}).encode())

if __name__ == "__main__":
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, ChatBotHandler)
    print("Server running on port 8000...")
    httpd.serve_forever()