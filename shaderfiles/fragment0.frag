#version 400

out vec4 finalColor;

in vec3 pos;
in vec4 inColor;
in vec3 outNormals;
in vec2 outTexCoords;
in vec3 vecToLight;
in vec3 vecToCamera;

uniform sampler2D texSampler;

uniform float damp;
int mode=1;

const vec3 lightPos=vec3(0.,1.,10.);
const vec3 lightColor=vec3(1.,1.,1.);
const float lightPower=2.;
const vec3 ambientColor=vec3(.1,0.,0.);
vec3 diffuseColor=inColor.xyz;
const vec3 specColor=vec3(1.,1.,.4);
const float shininess=16.;
const float screenGamma=2.2;

void main(){
    
    vec3 normal=normalize(outNormals);
    vec3 lightDir=normalize(vecToLight);
    float distance=length(lightDir);
    distance=distance*distance;
    
    float lambertian=max(dot(lightDir,normal),0.);
    float specular=0.;
    
    if(lambertian>0.){
        
        vec3 viewDir=normalize(-vecToCamera);
        
        // this is blinn phong
        vec3 halfDir=normalize(lightDir+viewDir);
        float specAngle=max(dot(halfDir,normal),0.);
        specular=pow(specAngle,shininess);
        
        // this is phong (for comparison)
        if(mode==2){
            vec3 reflectDir=reflect(-lightDir,normal);
            specAngle=max(dot(reflectDir,viewDir),0.);
            // note that the exponent is different here
            specular=pow(specAngle,shininess/4.);
        }
    }
    vec3 colorLinear=ambientColor+
    diffuseColor*
    lambertian*
    lightColor*
    lightPower/distance+
    specColor*
    specular*
    lightColor*
    lightPower/distance;
    // apply gamma correction (assume ambientColor, diffuseColor and specColor
    // have been linearized, i.e. have no gamma correction in them)
    vec3 colorGammaCorrected=pow(colorLinear,vec3(1./screenGamma));
    // use the gamma corrected color in the fragment
    finalColor=vec4(1.,.5,.6,1.);
    //finalColor=vec4(texture(texSampler,outTexCoords))*max(vec4(colorGammaCorrected,1.),vec4(ambientColor,1.));
}