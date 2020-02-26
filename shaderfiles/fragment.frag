#version 400

//
out vec4 finalColor;
//in
in vec3 color;
in vec2 outTexCoords;
in vec3 outNormals;
in vec3 vecToLight;
in vec3 vecToCamera;
in vec3 rgb;

uniform sampler2D texSampler;
float damp = 10;
float reflectivity = 2.5;
vec3 lightColor = vec3(1.0, 0.9, 0.9);

void main(){
    vec3 unitNormal = normalize(outNormals);
    vec3 unitLight = normalize(vecToLight);
    float ndot1 = dot(unitNormal, unitLight);
    float brightness = max(ndot1, 0.0);
    vec3 diffuseColor = lightColor * brightness;

    vec3 unitCamera = normalize(vecToCamera);
    vec3 incidentRay = -unitLight;
    incidentRay = normalize(incidentRay);
    vec3 reflectedRay = reflect(incidentRay, unitNormal);

    float specularFactor = dot(reflectedRay, unitCamera);
    specularFactor = max(specularFactor, 0.0);
    float specularDamper = pow(specularFactor, damp);
    vec3 finalSpecular = specularDamper * lightColor * reflectivity;

    finalColor = vec4(texture(texSampler, outTexCoords)) * vec4(diffuseColor + finalSpecular, 1.0);
    //finalColor=2*vec4(sin(rgb.x), sin(rgb.y), sin(rgb.z), 1.0)*vec4(diffuseColor+finalSpecular,1.);
}
