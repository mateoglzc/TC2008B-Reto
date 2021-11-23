using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Transformations : MonoBehaviour
{
    
    public static Vector4 MakeHomogenousVectors(Vector3 vect)
    {
        return new Vector4(vect.x, vect.y, vect.z, 1);
    }

    public static Matrix4x4 MakeTranslation(float x1, float y1, float z1)
    {
        Matrix4x4 mat = Matrix4x4.identity;
        
        mat[0,3] = x1;
        mat[1,3] = y1;
        mat[2,3] = z1;

        return mat;
    
    }
    public static Matrix4x4 MakeScale(float x1, float y1, float z1)
    {
        Matrix4x4 mat = Matrix4x4.identity;
        
        mat[0,0] = x1;
        mat[1,1] = y1;
        mat[2,2] = z1;

        return mat;
    }

    public static Matrix4x4 MakeRotationZ(float angle)
    {
        Matrix4x4 mat = Matrix4x4.identity;
        float rads = angle * Mathf.Deg2Rad;
        
        mat[0,0] = Mathf.Cos(rads);
        mat[0,1] = - Mathf.Sin(rads);
        mat[1,0] = Mathf.Sin(rads);
        mat[1,1] = Mathf.Cos(rads);

        return mat;
    }

    public static Matrix4x4 MakeRotationX(float angle)
    {
        Matrix4x4 mat = Matrix4x4.identity;
        float rads = angle * Mathf.Deg2Rad;
        
        mat[1,1] = Mathf.Cos(rads);
        mat[1,2] = - Mathf.Sin(rads);
        mat[2,1] = Mathf.Sin(rads);
        mat[2,2] = Mathf.Cos(rads);

        return mat;
    }

    public static Matrix4x4 MakeRotationY(float angle)
    {
        Matrix4x4 mat = Matrix4x4.identity;
        float rads = angle * Mathf.Deg2Rad;
        

        mat[0,0] = Mathf.Cos(rads);
        mat[0,2] = Mathf.Sin(rads);
        mat[2,0] = - Mathf.Sin(rads);
        mat[2,2] = Mathf.Cos(rads);


        return mat;
    }

}
