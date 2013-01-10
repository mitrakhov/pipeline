#ifndef __directlighintg__
#define __directlighintg__

#include "voplib.h"
#include "pbrexports.h"
#include "pbrpathtrace.h"
#include "math.h"

void direct_lighting(
        // Inputs
        bsdf fval;
        vector opac;
        vector pos;
        vector dir;
        int sid;
        float now;
        int isconnected_lightmask;
        string lightmask;
        int inmask;
        int inshadowmask;
        int doshadow;
        string mode;
        int multilight;

        // Outputs
        vector clr;
        vector noshadow;
        vector shadow;
        float nsam;
        int imask;
        vector dclr;
        vector rclr;
        vector tclr;
        vector sclr;
        vector vclr)
{
    int     lights[];
    int     light_map[];
    int     ismicropoly = 0;
    int     diffuselevel = getglobalraylevel();
    int     fakecaustics = 0;
    float   colorlimit = 1024;
    string  colorspace = "linear";
    int     n, i, idx;
    vector  dclr_t;
    vector  rclr_t;
    vector  tclr_t;
    vector  sclr_t;
    vector  vclr_t;
    string  engine;

    renderstate("renderer:colorlimit", colorlimit);
    renderstate("renderer:colorspace", colorspace);
    renderstate("object:fakecaustics", fakecaustics);
    if (getraylevel() == 0)
    {
        renderstate("renderer:renderengine", engine);
        ismicropoly = engine == "micropoly" ||
                       engine == "pbrmicropoly";
    }

    if (isconnected_lightmask)
        lights = getlights("lightmask", lightmask);
    else
        lights = getlights();

    int mask = inmask & getbounces(fval);
    int shadowmask = inshadowmask & getbounces(fval);

    n = arraylength(lights);

    FOR_ALL_EXPORTS3(EXPORT_DEF, direct, _l[]);
    FOR_ALL_EXPORTS3(EXPORT_RESIZE, direct, _l);

    vector  lclr;
    vector  lclr_l[];
    vector  lclr_t;
    resize(lclr_l, n);

    for (i = 0; i < n; i++)
    {
        FOR_ALL_EXPORTS3(EXPORT_ZERO, direct, _l[i])
        lclr_l[i] = {0,0,0};
        push(light_map, i);
    }

    lclr = 0;
    noshadow = 0;
    nsam = 0;
    imask = 0;

    if (mode == "multisample")
    {
        pbr_direct_lighting(
                lclr,
                lclr_l,
                nsam,
                imask,
                direct_diffuse_l,
                direct_specular_l,
                direct_reflect_l,
                direct_refract_l,
                direct_volume_l,
                sid,
                pos,
                fval,
                dir,
                normal_bsdf(fval),
                dPdz,
                now,
                {1,1,1},
                lights,
                light_map,
                mask,
                shadowmask,
                0,
                doshadow,
                multilight,
                fakecaustics,
                colorlimit,
                diffuselevel,
                1e6F,
                getraylevel() == 0,
                colorspace,
                ismicropoly);
    }
    else
    {
        vector      nml = normal_bsdf(fval);
        vector      col;
        vector      shadow_col;
        string      olmask;

        renderstate("object:lightmask", olmask);

        illuminance(pos, nml, PI,
                isconnected_lightmask ? lightmask : olmask)
        {
            shadow_col = Cl;

            idx = pbr_findlight(lights, getlightid(getlightname()), n);
            col = eval_bsdf(fval, -dir, normalize(L), mask);
            lclr_l[idx] += shadow_col * col;
            if (doshadow)
            {
                shadow(shadow_col);
            }
            col *= shadow_col;
            direct_diffuse_l[idx] += shadow_col * eval_bsdf(
                    fval, -dir, normalize(L), mask & PBR_DIFFUSE_MASK);
            direct_reflect_l[idx] += shadow_col * eval_bsdf(
                    fval, -dir, normalize(L), mask & PBR_GLOSSY_MASK);
            direct_refract_l[idx] += shadow_col * eval_bsdf(
                    fval, -dir, normalize(L), mask & PBR_GLOSSY_MASK);
            direct_volume_l[idx] += shadow_col * eval_bsdf(
                    fval, -dir, normalize(L), mask & PBR_VOLUME_MASK);
            lclr += col;
            nsam++;
        }
    }

    // Premultiply
    lclr *= opac;

    dclr_t = 0;
    rclr_t = 0;
    tclr_t = 0;
    sclr_t = 0;
    vclr_t = 0;
    lclr_t = 0;

    for (i = 0; i < n; i++)
    {
        idx = lights[i];

        dclr = direct_diffuse_l[i] * opac;
        rclr = direct_reflect_l[i] * opac;
        tclr = direct_refract_l[i] * opac;
        sclr = direct_specular_l[i] * opac;
        vclr = direct_volume_l[i] * opac;
        clr = dclr + rclr + tclr + sclr + vclr;
        noshadow = lclr_l[i] * opac;
        shadow = pbr_shadowmatte(clr, noshadow);
        dclr_t += dclr;
        rclr_t += rclr;
        tclr_t += tclr;
        sclr_t += sclr;
        vclr_t += vclr;
        lclr_t += noshadow;

        storelightexports(getlightname(idx));
    }

    dclr = dclr_t;
    rclr = rclr_t;
    tclr = tclr_t;
    sclr = sclr_t;
    vclr = vclr_t;
    clr = lclr;
    noshadow = lclr_t;
    shadow = pbr_shadowmatte(clr, lclr_t);
}

#endif //  __directlighting__