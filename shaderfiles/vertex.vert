#version 400

//in
in vec3 position;
in vec3 normals;
in vec2 texCoords;

//out
out vec3 color;
out vec2 outTexCoords;
out vec3 outNormals;
out vec3 vecToLight;
out vec3 vecToCamera;
out vec3 rgb;

//uniforms
uniform vec3 setColor;
uniform vec3 ambientC;
uniform mat4 transformationMatrix;
uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;

//locals


void main(){

    vec4 worldPosition = transformationMatrix*vec4(position.xyz, 1.0);
    vec3 lightpos=vec3(0.0, 0.0, 10.0);
    //gl_Position = vec4(position, 1.0);
    vec3 normal = (transformationMatrix*vec4(normals, 0.0)).xyz;
    vecToLight = lightpos - worldPosition.xyz;
    vecToCamera = (inverse(viewMatrix)*vec4(0.0, 0.0, 0.0, 1.0)).xyz - worldPosition.xyz;
    outNormals = normal;
    color = setColor;
    outTexCoords = texCoords;
    
    gl_Position=projectionMatrix*viewMatrix*worldPosition;
    rgb = gl_Position.xyz;
}
