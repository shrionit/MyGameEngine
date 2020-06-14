#version 400

out vec4 finalColor;

in vec3 pos;
in vec4 inColor;
in vec3 outNormals;
in vec2 outTexCoords;
in vec3 vecToLight;
in vec3 vecToCamera;

struct LightProp{
    vec3 lightcolor;
    vec3 ambientcolor;
    float shininess;
    float specdamp;
    int mode;
};

uniform sampler2D texSampler;

// uniform LightProp mainlight=LightProp(vec3(0.),vec3(0.),0.,0.,1);

uniform vec3 lightColor=vec3(.9059,.7608,.6745);
uniform vec3 ambient=vec3(.6196,.5059,.5059);
uniform float shininess=20.;
uniform float specDamp=5.;
uniform int blinn=1;
/* Coordinate and unit utils */

float near=.1;
float far=1000.;

float LinearizeDepth(float depth){
    float z=depth*2.-1.;// back to NDC
    return(2.*near*far)/(far+near-z*(far-near));
}

void main(){
    float diff=max(dot(outNormals,vecToLight),0.);
    vec3 diffuse=diff*lightColor;
    
    float spec=0.;
    if(blinn==1){
        vec3 halfwayDir=normalize(vecToLight+vecToCamera);
        spec=pow(max(dot(outNormals,halfwayDir),0.),shininess);
    }
    else{
        vec3 reflectDir=reflect(-vecToLight,outNormals);
        spec=pow(max(dot(vecToCamera,reflectDir),0.),shininess);
    }
    vec3 specular=specDamp*spec*lightColor;
    
    vec4 color=texture(texSampler,outTexCoords);
    
    vec3 result=(ambient+diffuse+specular)*color.rgb;
    gl_FragColor=vec4(result,color.a);
    
    // float depth=LinearizeDepth(gl_FragCoord.z)/far;
    // gl_FragColor=vec4(vec3(depth),color.a);
}