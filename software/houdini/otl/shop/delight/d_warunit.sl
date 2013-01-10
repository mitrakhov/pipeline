surface
d_warunit( 
	string	colorMap="";
	
	float	diffuseIntensity=1;
	color	diffuseColor=color "rgb" (1,1,1);
	
	float	occlusionSwitch=0;
	float	occlusionMaxDist=-1;
	float	occlusionFalloff=0;
	float	occlusionNSamples=64;
	float	occlusionConeAngle=90;
	float	occlusionAdaptive=0;
	float	occlusionScale=1;
	uniform vector sky = vector (0, 0, 0);		
	
	float	specurIntensity=1;
	color	specularColor=color "rgb" (1,1,1);
	float	specularSize=50;
	string	specularMap="";
	
	float	envIntensity=1;
	string	envMap="";
	color	envTint=color "rgb"(1,1,1);
	float	envBlur=0;
)
	
{
normal Nn = normalize(N);
vector In = -normalize(I);

color _colorMap = texture(colorMap );

color _diffuse=diffuseIntensity*diffuseColor*diffuse(Nn);

if (occlusionSwitch==1){
	float _occlusion = occlusion( P, Ng, occlusionNSamples, "bias", 0.001, "maxdist", occlusionMaxDist, "falloff", occlusionFalloff, "coneangle", radians(occlusionConeAngle), "adaptive", occlusionAdaptive, "axis", sky );
	}
	else float _occlusion=0;

color _specularMap=texture(specularMap);
color _specular=specurIntensity*specularColor*_specularMap*specular(Nn,In,specularSize);

vector Nf = faceforward( N, I );
color _environment = envIntensity*environment( envMap, vtransform("world", Nf), "blur", envBlur)*envTint*_specularMap;
	
	Oi = Os;
	Ci =Cs*Os*_colorMap*_diffuse*(1-occlusionScale*_occlusion)+_specular+pow(occlusion(P,reflect(In,Nn), 20,  "coneangle", PI/5),2.5)*_environment;
//	Ci =Cs*Os*_colorMap*_diffuse+_specular+_environment;
//	Ci=(1-occlusionScale*_occlusion);
}
