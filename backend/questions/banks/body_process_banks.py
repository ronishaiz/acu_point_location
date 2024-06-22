import os.path

from backend.enums import Organ
from backend.questions.body_process import BodyProcess, body_process_pictures_folder

blood_formation_process = BodyProcess(_picture_file_name='blood_formation.png',
                                      _organ_to_related_points={
                                          Organ.SP: {"ST36": "To harmonize the MJ and support post-heaven Qi and Blood",
                                                     "CV12": "To harmonize the MJ",
                                                     "SP3": "To strengthen all SP functions",
                                                     "BL20": "To strengthen all SP functions",
                                                     "SP2": "As a tonification point of the Earth element, to strengthen the SP",
                                                     "SP10": "As a point supporting the blood",
                                                     "CV6": "To strengthen Yang and help the SP with the T&T",
                                                     "GV4": "To strengthen Yang and help the SP with the T&T",
                                                     "GV20": "To strengthen Yang and help the SP with the T&T",
                                                     "SP4": "To harmonize the MJ, sooth, and do well with the Chong MAI (sea of blood)"},
                                          Organ.ST: {"ST36": "To harmonize the MJ and support post-heaven Qi and Blood",
                                                     "CV12": "To harmonize the MJ",
                                                     "ST21": "In case food stagnation is the cause for the malfunction in the Blood formation",
                                                     "ST34": "To harmonize ST Qi"},
                                          Organ.LU: {"CV17": "To move Qi at the chest and support the pushing of Zhong Qi from the LU to the HT",
                                                     "CV15": "To move Qi at the chest and support the pushing of Zhong Qi from the LU to the HT",
                                                     "LU9": "To strengthen all LU functions",
                                                     "BL13": "To strengthen all LU functions"},
                                          Organ.HT: {"HT7": "To strengthen all HT functions",
                                                     "BL15": "To strengthen all HT functions",
                                                     "CV17": "To move Qi at the chest area and support the HT pumping",
                                                     "SP6": "To support HT Yin",
                                                     "CV4": "To support Yin and Blood in the body",
                                                     "HT6": "To support HT Yin and Blood",
                                                     "HT8": "To strengthen the HT as the HORARY point and the Fire point (5 elements perspective)",
                                                     "HT5": "To balance HT Qi in cases of arrhythmia",
                                                     "HT4": "To sooth the Shen",
                                                     "HT3": "To help in cases of depression and trauma causing Blood Xu"},
                                          Organ.KID: {"KID3": "To strengthen all KID functions",
                                                      "BL23": "To strengthen all KID functions",
                                                      "GV4": "To strengthen KID Yang (Yuan Qi)",
                                                      "GV16": "Sea of Marrow",
                                                      "GV20": "Sea of Marrow",
                                                      "CV4": "Guan Yuan - will strengthen Yuan Qi",
                                                      "BL11": "Meeting of Marrow",

                                                      # TODO: add more KID points after learning the meridian
                                                      }
                                      })

qi_formation_process = BodyProcess(_picture_file_name='qi_formation.jpg',
                                   _organ_to_related_points={
                                       Organ.SP: {"ST36": "To harmonize the MJ and support post-heaven Qi",
                                                  "CV12": "To harmonize the MJ",
                                                  "SP3": "To strengthen all SP functions",
                                                  "BL20": "To strengthen all SP functions",
                                                  "SP2": "As a tonification point of the Earth element, to strengthen the SP",
                                                  "CV6": "To strengthen Yang and Qi and help the SP with the T&T",
                                                  "GV4": "To strengthen Yang and Qi help the SP with the T&T",
                                                  "GV20": "To strengthen Yang and help the SP with the T&T"},
                                       Organ.ST: {"ST36": "To harmonize the MJ and support post-heaven Qi and Blood",
                                                  "CV12": "To harmonize the MJ",
                                                  "ST21": "In case food stagnation is the cause for the malfunction in the Blood formation",
                                                  "ST34": "To harmonize ST Qi"},
                                       Organ.LU: {"CV17": "To move Qi at the chest and support the pushing of Zhong Qi from the LU to the HT",
                                                  "CV15": "To move Qi at the chest and support the pushing of Zhong Qi from the LU to the HT",
                                                  "LU9": "To strengthen all LU functions",
                                                  "BL13": "To strengthen all LU functions",
                                                  "LU7": "To help the LU with the function of downing and distributing the Qi",
                                                  "ST40": "To help remove fluid from the LU and allow it to work properly"},
                                       Organ.KID: {"KID3": "To strengthen all KID functions",
                                                   "BL23": "To strengthen all KID functions",
                                                   "GV4": "To strengthen KID Yang (Yuan Qi)",
                                                   "CV4": "Guan Yuan - will strengthen Yuan Qi",
                                                   }
                                   })

body_fluid_transformation_process = BodyProcess(_picture_file_name='body_fluid_transformation.png',
                                                _organ_to_related_points={
                                                    Organ.SP: {"SP9": "To get rid of excess of fluids in low burner (via the BL)",
                                                               "LU1": "To help with excessive fluids in the LU, originating from SP deficiency",
                                                               "SP3": "To strengthen all SP functions",
                                                               "BL20": "To strengthen all SP functions",
                                                               "SP2": "As a tonification point of the Earth element, to strengthen the SP",
                                                               "CV6": "To strengthen Yang and Qi and help the SP with the T&T",
                                                               "GV4": "To strengthen Yang and Qi help the SP with the T&T",
                                                               "GV20": "To strengthen Yang and help the SP with the T&T"
                                                               },
                                                    Organ.ST: {"ST36": "To harmonize the MJ and support post-heaven Qi and Blood",
                                                               "CV12": "To harmonize the MJ",
                                                               "ST21": "In case food stagnation is the cause for the malfunction in the Blood formation",
                                                               "ST34": "To harmonize ST Qi",
                                                               },
                                                    Organ.LU: {"ST40": "To get rid of excess of fluids in the high burner",
                                                               "SP5": "To extract phlegm from the LU",
                                                               "LU9": "To strengthen all LU functions",
                                                               "BL13": "To strengthen all LU functions",
                                                               "LU7": "To help the LU with the function of downing and distributing the Qi (and fluid)"},
                                                    Organ.SI: {"BL27": "To strengthen all SI functions",
                                                               "SI4": "As a SI Yuan point"},
                                                    Organ.LI: {"BL25": "To strengthen all LI functions"},
                                                    Organ.BL: {"ST28": "To move fluids in lower burner",
                                                               "CV3": "BL MU point",
                                                               "BL28": "To strengthen all BL functions",
                                                               "BL64": "To strengthen all BL functions",
                                                               "BL66": "To extract heat from the BL"},
                                                    Organ.KID: {"KID3": "To strengthen all KID functions",
                                                                "BL23": "To strengthen all KID functions",
                                                                "GV4": "To strengthen KID Yang (Yuan Qi)",
                                                                "CV4": "Guan Yuan - will strengthen Yuan Qi",
                                                                # TODO: add more KID points after learning the meridian
                                                                }
                                                })

process_name_to_process = {process.process_name: process
                           for process in [blood_formation_process, qi_formation_process, body_fluid_transformation_process]}

all_organs = set([organ for process in process_name_to_process.values() for organ in process.organs])

organ_to_picture_path = {
    organ: os.path.join(body_process_pictures_folder, organ.value) for organ in all_organs
}
