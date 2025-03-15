#pragma once
#include <complex>

struct Vector3
{
    float x, y, z;

    Vector3() : x(0.0f), y(0.0f), z(0.0f) {}
    Vector3(float x, float y, float z) : x(x), y(y), z(z) {}

    Vector3 operator+(const Vector3& other) const
    {
        return Vector3(x + other.x, y + other.y, z + other.z);
    }

    Vector3 operator-(const Vector3& other) const
    {
        return Vector3(x - other.x, y - other.y, z - other.z);
    }

    Vector3 operator*(float scalar) const
    {
        return Vector3(x * scalar, y * scalar, z * scalar);
    }

    Vector3 operator/(float scalar) const
    {
        return Vector3(x / scalar, y / scalar, z / scalar);
    }

    Vector3 cross(const Vector3& other) const
    {
        return Vector3(
            y * other.z - z * other.y,
            z * other.x - x * other.z,
            x * other.y - y * other.x
        );
    }

    float dot(const Vector3& other) const
    {
        return x * other.x + y * other.y + z * other.z;
    }

    float magnitude() const
    {
        return std::sqrt(x * x + y * y + z * z);
    }

    Vector3 normalized() const
    {
        float mag = magnitude();
        if (mag > 0.0f)
            return Vector3(x / mag, y / mag, z / mag);
        return Vector3();
    }
};