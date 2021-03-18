import FWCore.ParameterSet.Config as cms

uct2016EmulatorDigis = cms.EDProducer('L1TCaloSummary',
                                      ecalToken = cms.InputTag("simEcalTriggerPrimitiveDigis"),
                                      hcalToken = cms.InputTag("simHcalTriggerPrimitiveDigis"),
                                      useLSB = cms.bool(True),
                                      useCalib = cms.bool(True),
                                      useECALLUT = cms.bool(True),
                                      useHCALLUT = cms.bool(True),
                                      useHFLUT = cms.bool(True),
                                      nPumBins = cms.uint32(18),
pumLUT00n=  cms.vdouble(0.43, 0.32, 0.29, 0.36, 0.33, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25),
pumLUT00p=  cms.vdouble(0.45, 0.32, 0.29, 0.35, 0.31, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25),
pumLUT01n=  cms.vdouble(0.60, 0.39, 0.33, 0.44, 0.39, 0.26, 0.27, 0.26, 0.26, 0.25, 0.25, 0.25, 0.25),
pumLUT01p=  cms.vdouble(0.60, 0.39, 0.33, 0.41, 0.35, 0.26, 0.27, 0.26, 0.26, 0.25, 0.25, 0.25, 0.25),
pumLUT02n=  cms.vdouble(0.76, 0.52, 0.46, 0.57, 0.52, 0.33, 0.41, 0.34, 0.31, 0.29, 0.27, 0.26, 0.25),
pumLUT02p=  cms.vdouble(0.75, 0.52, 0.46, 0.55, 0.48, 0.34, 0.42, 0.34, 0.31, 0.29, 0.27, 0.26, 0.25),
pumLUT03n=  cms.vdouble(0.90, 0.63, 0.56, 0.69, 0.62, 0.39, 0.58, 0.41, 0.37, 0.33, 0.29, 0.27, 0.25),
pumLUT03p=  cms.vdouble(0.90, 0.64, 0.56, 0.66, 0.57, 0.39, 0.58, 0.41, 0.37, 0.33, 0.29, 0.26, 0.25),
pumLUT04n=  cms.vdouble(1.03, 0.74, 0.66, 0.80, 0.72, 0.45, 0.80, 0.50, 0.45, 0.39, 0.32, 0.28, 0.25),
pumLUT04p=  cms.vdouble(1.03, 0.76, 0.67, 0.77, 0.67, 0.46, 0.81, 0.50, 0.45, 0.39, 0.32, 0.27, 0.25),
pumLUT05n=  cms.vdouble(1.17, 0.86, 0.77, 0.92, 0.83, 0.53, 1.09, 0.60, 0.55, 0.47, 0.37, 0.29, 0.26),
pumLUT05p=  cms.vdouble(1.18, 0.88, 0.77, 0.89, 0.77, 0.54, 1.10, 0.61, 0.55, 0.47, 0.35, 0.29, 0.26),
pumLUT06n=  cms.vdouble(1.32, 0.98, 0.88, 1.04, 0.93, 0.61, 1.44, 0.72, 0.66, 0.57, 0.42, 0.31, 0.26),
pumLUT06p=  cms.vdouble(1.32, 1.00, 0.89, 1.01, 0.88, 0.63, 1.46, 0.73, 0.67, 0.57, 0.41, 0.30, 0.26),
pumLUT07n=  cms.vdouble(1.47, 1.11, 1.01, 1.17, 1.05, 0.71, 1.86, 0.86, 0.81, 0.69, 0.50, 0.34, 0.27),
pumLUT07p=  cms.vdouble(1.48, 1.14, 1.01, 1.13, 0.99, 0.73, 1.89, 0.87, 0.82, 0.70, 0.47, 0.33, 0.27),
pumLUT08n=  cms.vdouble(1.63, 1.26, 1.14, 1.30, 1.17, 0.82, 2.37, 1.02, 0.98, 0.85, 0.59, 0.37, 0.28),
pumLUT08p=  cms.vdouble(1.64, 1.28, 1.15, 1.26, 1.11, 0.85, 2.41, 1.03, 0.99, 0.86, 0.56, 0.36, 0.28),
pumLUT09n=  cms.vdouble(1.81, 1.41, 1.28, 1.45, 1.31, 0.95, 2.98, 1.20, 1.18, 1.03, 0.71, 0.42, 0.30),
pumLUT09p=  cms.vdouble(1.82, 1.45, 1.29, 1.41, 1.24, 0.98, 3.02, 1.21, 1.19, 1.05, 0.67, 0.40, 0.29),
pumLUT10n=  cms.vdouble(2.01, 1.58, 1.43, 1.62, 1.45, 1.10, 3.70, 1.41, 1.42, 1.26, 0.87, 0.48, 0.32),
pumLUT10p=  cms.vdouble(2.02, 1.61, 1.46, 1.58, 1.38, 1.13, 3.73, 1.42, 1.43, 1.27, 0.82, 0.46, 0.31),
pumLUT11n=  cms.vdouble(2.24, 1.78, 1.61, 1.78, 1.60, 1.27, 4.55, 1.64, 1.71, 1.55, 1.08, 0.57, 0.36),
pumLUT11p=  cms.vdouble(2.21, 1.82, 1.63, 1.75, 1.53, 1.31, 4.67, 1.67, 1.71, 1.57, 1.01, 0.54, 0.36),
pumLUT12n=  cms.vdouble(2.50, 2.00, 1.82, 1.91, 1.81, 1.56, 5.56, 1.85, 2.01, 1.87, 1.31, 0.68, 0.42),
pumLUT12p=  cms.vdouble(2.44, 2.02, 1.90, 2.01, 1.70, 1.51, 5.61, 1.96, 2.04, 1.80, 1.24, 0.65, 0.43),
pumLUT13n=  cms.vdouble(2.96, 2.40, 2.14, 2.41, 2.01, 1.76, 8.05, 2.41, 2.43, 2.17, 1.67, 0.90, 0.59),
pumLUT13p=  cms.vdouble(3.28, 2.64, 2.26, 2.23, 1.97, 1.89, 7.61, 2.27, 2.33, 2.26, 1.44, 0.79, 0.52),
pumLUT14n=  cms.vdouble(2.96, 2.40, 2.14, 2.41, 2.01, 1.76, 8.05, 2.41, 2.43, 2.17, 1.67, 0.90, 0.59),
pumLUT14p=  cms.vdouble(3.28, 2.64, 2.26, 2.23, 1.97, 1.89, 7.61, 2.27, 2.33, 2.26, 1.44, 0.79, 0.52),
pumLUT15n=  cms.vdouble(2.96, 2.40, 2.14, 2.41, 2.01, 1.76, 8.05, 2.41, 2.43, 2.17, 1.67, 0.90, 0.59),
pumLUT15p=  cms.vdouble(3.28, 2.64, 2.26, 2.23, 1.97, 1.89, 7.61, 2.27, 2.33, 2.26, 1.44, 0.79, 0.52),
pumLUT16n=  cms.vdouble(2.96, 2.40, 2.14, 2.41, 2.01, 1.76, 8.05, 2.41, 2.43, 2.17, 1.67, 0.90, 0.59),
pumLUT16p=  cms.vdouble(3.28, 2.64, 2.26, 2.23, 1.97, 1.89, 7.61, 2.27, 2.33, 2.26, 1.44, 0.79, 0.52),
pumLUT17n=  cms.vdouble(2.96, 2.40, 2.14, 2.41, 2.01, 1.76, 8.05, 2.41, 2.43, 2.17, 1.67, 0.90, 0.59),
pumLUT17p=  cms.vdouble(3.28, 2.64, 2.26, 2.23, 1.97, 1.89, 7.61, 2.27, 2.33, 2.26, 1.44, 0.79, 0.52),
                                      caloScaleFactor = cms.double(0.5),
                                      jetSeed = cms.uint32(10),
                                      tauSeed = cms.uint32(10),
                                      tauIsolationFactor = cms.double(0.3),
                                      eGammaSeed = cms.uint32(5),
                                      eGammaIsolationFactor = cms.double(0.3),
                                      verbose = cms.bool(False),
                                      # See UCTLayer1.hh for firmware version
                                      firmwareVersion = cms.int32(1)
                                      )
