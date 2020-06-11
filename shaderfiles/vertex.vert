#version 400
//vectors
in vec3 position;
in vec3 normals;
in vec2 texCoords;
in vec3 indices;

out vec4 inColor;
out vec3 pos;
out vec3 outNormals;
out vec2 outTexCoords;
out vec3 vecToLight;
out vec3 vecToCamera;

//uniforms
uniform mat4 modelMatrix;
uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;

uniform vec3 lightPos=vec3(0.,5.,0.);

void main(){
    vec4 worldPosition=modelMatrix*vec4(position,1.);
    vec3 viewPos=(inverse(viewMatrix)*vec4(0.,0.,0.,1.)).xyz;
    vec3 normal=normalize((modelMatrix*vec4(normals,0.)).xyz);
    
    vecToLight=normalize(lightPos-worldPosition.xyz);
    vecToCamera=normalize(viewPos-worldPosition.xyz);
    
    vec4 finalMatrix=projectionMatrix*viewMatrix*worldPosition;
    
    gl_Position=finalMatrix;
    
    pos=finalMatrix.xyz;
    outNormals=normal;
    outTexCoords=texCoords;
}