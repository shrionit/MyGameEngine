#version 400
out vec4 finalColor;

in vec2 texCord;

uniform float gamma=1.;

uniform sampler2D screenTexture;
uniform float kernel[9]=float[](
    0.,0.,0.,
    0.,1.,0.,
    0.,0.,0.
);

float offset=1./300.;

vec3 applyKernelToSample(float kernel[9],vec3 sampleTex[9]){
    vec3 col=vec3(0.);
    for(int i=0;i<9;i++)col+=sampleTex[i]*kernel[i];
    return col;
}

float[9]applyOpOn(float arr[9],int op,float operand){
    for(int i=0;i<9;i++){
        switch(op){
            case 0:
            arr[i]+=operand;
            break;
            case 1:
            arr[i]-=operand;
            break;
            case 2:
            arr[i]*=operand;
            break;
            case 3:
            arr[i]/=operand;
            break;
            default:
            arr[i]=operand;
        }
    }
    return arr;
}

vec2[9]genOffset(float offset){
    return vec2[](
        vec2(-offset,offset),// top-left
        vec2(0.f,offset),// top-center
        vec2(offset,offset),// top-right
        vec2(-offset,0.f),// center-left
        vec2(0.f,0.f),// center-center
        vec2(offset,0.f),// center-right
        vec2(-offset,-offset),// bottom-left
        vec2(0.f,-offset),// bottom-center
        vec2(offset,-offset)// bottom-right
    );
}

vec3 blackNwhite(vec3 v){
    float a=0.;
    for(int i=0;i<3;i++){
        a+=v[i];
    }
    return vec3(a/3.);
}

vec3 greyscale(vec3 c){
    return vec3(.2126*c.r+.7152*c.g+.0722*c.b);
}

void main(){
    vec3 mcolor=vec3(texture(screenTexture,texCord));
    vec2[9]offsets=genOffset(offset);
    vec3 sampleTex[9];
    for(int i=0;i<9;i++){
        sampleTex[i]=vec3(texture(screenTexture,texCord.st+offsets[i]));
    }
    
    mcolor=applyKernelToSample(kernel,sampleTex);
    
    mcolor=pow(mcolor,vec3(1/gamma));
    
    finalColor=vec4(mcolor,1.);
}