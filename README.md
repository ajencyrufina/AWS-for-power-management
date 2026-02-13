**⚡ AWS-Based Power Consumption Monitoring System**

**📌 Project Overview**

This project implements a real-time power consumption monitoring system using AWS Cloud services. The system collects power usage data from a device (sensor/microcontroller/simulator), sends it to AWS, stores it in the cloud, and allows users to monitor energy consumption remotely.

The goal of this project is to demonstrate how IoT + Cloud Computing can be used for smart energy monitoring and analytics.

**🎯 Objectives**

Monitor real-time power consumption data

Send device data securely to AWS Cloud

Store and process energy readings

Visualize and analyze consumption trends

Enable remote access to power usage information

**🏗️ System Architecture**

Power Sensor / Simulator

        ↓
Microcontroller (ESP32 / Device)

        ↓
AWS IoT Core (MQTT Protocol)

        ↓
AWS Lambda

        ↓
DynamoDB / S3

        ↓
Web Dashboard / Cloud Monitoring


**🛠️ Technologies Used**

🔹 Hardware

ESP32 / Arduino (or simulator)

Voltage & Current Sensors (if applicable)

🔹 Cloud Services (AWS)

AWS IoT Core

AWS Lambda

Amazon DynamoDB

Amazon S3 (optional)

Amazon CloudWatch

🔹 Programming

Python

Embedded C / Arduino IDE (if hardware used)

MQTT Protocol

**⚙️ How It Works**

The device measures power parameters (Voltage, Current, Power).

Data is sent securely using MQTT to AWS IoT Core.

AWS IoT triggers a Lambda function.

Lambda processes and stores data in DynamoDB.

Data can be visualized via dashboard or AWS console.

**📊 Features**

Real-time data transmission

Secure device authentication using certificates

Cloud-based data storage

Scalable architecture

Remote monitoring capability

Low-latency communication using MQTT

**🔐 Security Implementation**

X.509 certificate authentication

IAM roles for controlled access

Secure MQTT communication (TLS)

Restricted database access policies

**🚀 Setup Instructions**

1️⃣ Clone the Repository
git clone https://github.com/ajencyrufina/AWS-for-power-management.git
cd AWS-for-power-management

2️⃣ AWS Setup

Create a Thing in AWS IoT Core

Download device certificates

Attach IoT policies

Create DynamoDB table

Create Lambda function

Configure IoT Rule to trigger Lambda

3️⃣ Run Device Code

Upload firmware / run Python script to publish data to AWS IoT endpoint.

📈 Sample Data Format
{
  "device_id": "device001",
  "voltage": 230,
  "current": 1.5,
  "power": 345,
  "timestamp": "2026-02-13T10:30:00Z"
}

**📌 Future Enhancements**

Add mobile app dashboard

Implement anomaly detection using AWS ML

Add energy consumption prediction

Integrate SMS/email alerts

Multi-device monitoring support

**📚 Learning Outcomes**

Hands-on experience with AWS IoT Core

Understanding of cloud-based IoT architecture

Secure device-cloud communication

Serverless computing using Lambda

NoSQL database usage (DynamoDB)

**👩‍💻 Author**

Jency Rufina A

B.Tech – Electrical and Computer Science Engineering

VIT Chennai
