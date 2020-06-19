import FWCore.ParameterSet.Config as cms

bmtfKalmanTrackingSettings = cms.PSet(
    verbose = cms.bool(True),  # 
    lutFile = cms.string("L1Trigger/L1TMuon/data/bmtf_luts/kalmanLUTs.root"),

    # New Primitives
    initialK = cms.vdouble(-0.0681, -0.0968, -0.148, -0.266),
    initialK2 = cms.vdouble(1.204e-05, 2.627e-05, 1.225e-4, 6.173e-4),
    eLoss = cms.vdouble(7.7586e-4,0,0,0),

    aPhi = cms.vdouble(36.710, 0.29151, 0.3041, 0.21069),
    aPhiB = cms.vdouble(-27.517, -2.34376, -2.87148, -2.53521),
    aPhiBNLO = cms.vdouble(1.5679e-4, 0, 0, 0),

    bPhi = cms.vdouble(-1, .182, .209, .173),
    bPhiB = cms.vdouble(-1, 1.182, 1.209, 1.173),
    phiAt2 = cms.double(0.1396),
    etaLUT0 = cms.vdouble(8.946,7.508,6.279,6.399),
    etaLUT1 = cms.vdouble(0.159,0.116,0.088,0.128),

    #generic cuts
    #TODO: Rederive chi2 cuts (current is approx. scaling)
    chiSquare = cms.vdouble(0, 2.269, 4.680, 6.661),
    chiSquareCutPattern = cms.vint32(7,11,13,14,15),
    chiSquareCutCurvMax = cms.vint32(2500,2500,2500,2500,2500),
    chiSquareCut = cms.vint32(164,164,164,52,52),

    #vertex cuts
    trackComp = cms.vdouble(-5.367, -3.460, -1.408, -0.604),
    trackCompErr1 = cms.vdouble(1.8409, 2.2599, 2.1162, 1.4874),
    trackCompErr2 = cms.vdouble(0.55314, 0.50953, 0.52020, 0.60119),
    trackCompCutPattern = cms.vint32(3,5,6,9,10,12),   
    trackCompCutCurvMax = cms.vint32(34,34,34,34,34,34),   #this is shifted<<4
    trackCompCut        = cms.vint32(13,15,9,15,15,11),  
    chiSquareCutTight   = cms.vint32(33,65,39,164,164,39),  


    combos4=cms.vint32(9,10,11,12,13,14,15),
    combos3=cms.vint32(5,6,7),
    combos2=cms.vint32(3),
    combos1=cms.vint32(), #for future possible usage

    useOfflineAlgo = cms.bool(True),   

    mScatteringPhi = cms.vdouble(1.092,.02399,.01531,0.006009),
#    mScatteringPhi = cms.vdouble(3.633, 0.0678, 0.0320, 0.0129),
    mScatteringPhiB = cms.vdouble(3.167,1.518,1.951,1.807),
#    mScatteringPhiB = cms.vdouble(1.085, 0.552, 0.725, 0.750),
    # Assuming 0.01cm resolution
    pointResolutionPhi = cms.vdouble(3.579, 2.56, 1.751, 1.273),
    # Assuming 7 mrad resolution
    pointResolutionPhiB = cms.double(328833.),
    pointResolutionVertex = cms.double(1.),


    # Total bits, signed
    bitsPhi = cms.int32(17),
    bitsPhiB = cms.int32(12),
    phiBScale = cms.int32(56),
)



simKBmtfDigis = cms.EDProducer("L1TMuonBarrelKalmanTrackProducer",
    src = cms.InputTag("simPhase2KBmtfStubs"),
    bx = cms.vint32(-2,-1,0,1,2),
#    bx = cms.vint32(0),
    algoSettings = bmtfKalmanTrackingSettings,
    trackFinderSettings = cms.PSet(
        sectorsToProcess = cms.vint32(0,1,2,3,4,5,6,7,8,9,10,11),
        verbose = cms.int32(1),
        sectorSettings = cms.PSet(
#            verbose = cms.int32(1),
            verbose = cms.int32(0),
            wheelsToProcess = cms.vint32(-2,-1,0,1,2),
            regionSettings = cms.PSet(
                verbose=cms.int32(0)
            )
        )
        
    )
)
