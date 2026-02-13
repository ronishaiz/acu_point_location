from backend.enums import Organ, MeridianName

location_to_meridians = {
    Organ.LU.value: {
        MeridianName.LU: "",
        MeridianName.LI: "",
        MeridianName.HT: "",
        MeridianName.KID: "",
        MeridianName.LIV: "",
    },
    Organ.LI.value: {
        MeridianName.LU: "",
        MeridianName.LI: "",
    },
    Organ.SP.value: {
        MeridianName.SP: "",
        MeridianName.ST: ""
    },
    Organ.ST.value: {
        MeridianName.SP: "",
        MeridianName.ST: "",
        MeridianName.LU: "",
        MeridianName.SI: "",
        MeridianName.LIV: ""
    },
    Organ.HT.value: {
        MeridianName.HT: "",
        MeridianName.SI: "",
        MeridianName.SP: ""
    },
    Organ.SI.value: {
        MeridianName.HT: "",
        MeridianName.SI: ""
    },
    Organ.KID.value: {
        MeridianName.KID: "",
        MeridianName.BL: ""
    },
    Organ.BL.value: {
        MeridianName.KID: "",
        MeridianName.BL: ""
    },
    Organ.LIV.value: {
        MeridianName.LIV: "",
        MeridianName.GB: "",
    },
    Organ.GB.value: {
        MeridianName.LIV: "",
        MeridianName.GB: "",
    },
    Organ.PC.value: {
        MeridianName.PC: "",
        MeridianName.TW: ""
    },
    Organ.TW.value: {
        MeridianName.TW: "",
        MeridianName.PC: ""
    },
    "Nose": {
        MeridianName.LI: "LI20, side of the nose, opens nasal passages",
        MeridianName.ST: "Inner path starts at LI20 and connects it to the inner cantos of the eye"
    },
    "Base of the tongue": {
        MeridianName.SP: "Inner path ends there",
        MeridianName.CV: "Reaches there through CV23",
        MeridianName.GV: "Reaches there through GV15",
        MeridianName.HT: "Inner path is approximate to the tongue",
        MeridianName.KID: "Inner path ends there"
    },
    "Inner cantos of the eye": {
        MeridianName.ST: "Inner and outer paths are there",
        MeridianName.SI: "Inner path ends there",
        MeridianName.BL: "Outer path starts there",
        MeridianName.GB: "Inner path reaches there"
    },
    "Outer cantos of the eye": {
        MeridianName.SI: "Outer path gets there",
        MeridianName.TW: "Inner path ends there",
        MeridianName.GB: "Outer path starts there"
    },
    "Eye": {
        MeridianName.BL: "Outer path starts there",
        MeridianName.ST: "Inner and outer paths are there",
        MeridianName.SI: "Inner and outer paths are there",
        MeridianName.HT: "Inner path ends there",
        MeridianName.LIV: "Inner path reaches there",
    },
    "Lips and mouth": {
        MeridianName.ST: "Goes around the lips",
        MeridianName.LI: "Passes above the lips and switches sides",
        MeridianName.CV: "Ends below the lips in the mento-labial grove",
        MeridianName.GV: "Ends above the lips",
        MeridianName.LIV: "Inner path reaches there"
    },
    "Jaw": {
        MeridianName.ST: "At the angle of the mandible and the jaw",
        MeridianName.SI: "Reaches the angle of the mandible (SI17)",
    },
    "Cheek": {
        MeridianName.ST: "Outer path passes there",
        MeridianName.LI: "Outer path passes there",
        MeridianName.HT: "Inner path passes there",
        MeridianName.LIV: "Inner path passes there",
        MeridianName.TW: "Inner path passes there",
    },
    "Ear": {
        MeridianName.ST: "Outer path passes near the anterior border",
        MeridianName.BL: "Inner path goes inside the ear",
        MeridianName.SI: "Outer path ends near the tragus (SI19)",
        MeridianName.GB: "Outer path reaches there (GB2)",
        MeridianName.TW: "Outer path reaches there (TW17, TW21)",
    },
    "Head": {
        MeridianName.ST: "Outer path reaches there (ST8)",
        MeridianName.BL: "Goes around the head, posterior and anterior (both inner and outer)",
        MeridianName.GV: "Goes around the head, posterior and anterior (both inner and outer)",
        MeridianName.GB: "Lateral part of the head",
        MeridianName.TW: "Lateral part of the head",
        MeridianName.LIV: "Inner path reaches DU20"
    },
    "Hypochondrium": {
        MeridianName.LIV: "Inner path reaches there",
        MeridianName.GB: "Outer path reaches there",
    },
    "Neck": {
        MeridianName.ST: "Outer path passes there (ST9)",
        MeridianName.LI: "Outer path passes there (LI8)",
        MeridianName.GB: "Outer path reaches there (GB20)",
        MeridianName.SI: "Outer path reaches there (SI16, SI17)",
        MeridianName.TW: "Outer path reaches there (TW16)",
        MeridianName.BL: "Outer path reaches there (BL10)",
        MeridianName.CV: "Outer path reaches there (CV23)",
        MeridianName.GV: "Outer path reaches there (GV15, GV16)",
        MeridianName.LIV: "Inner path reaches there",
        MeridianName.KID: "Inner path reaches there",
        MeridianName.HT: "Inner path passes there",
    }
}