import FWCore.ParameterSet.Config as cms

bmtfKalmanTrackingSettings = cms.PSet(
    verbose = cms.bool(False),  # 
    lutFile = cms.string("L1Trigger/L1TMuon/data/bmtf_luts/kalmanLUTs.root"),

    # New Primitives
    initialK = cms.vdouble(-0.0628, -0.0869, -0.122, -0.272),
    initialK2 = cms.vdouble(-1.385e-05, -2.985e-05, -1.402e-4, -4.923e-4),
    eLoss = cms.vdouble(0.00078,0,0,0),
    
    aPhi = cms.vdouble(34.241, 0.283, 0.307, 0.183),
    aPhiB = cms.vdouble(-29.027, -2.459, -3.002, -2.597),
    aPhiBNLO = cms.vdouble(3.427e-4,0,0,0),

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
    chiSquareCut = cms.vint32(126*20,126*20,126*20,40*20,40*20),

    #vertex cuts
    trackComp = cms.vdouble(-5.367, -3.460, -1.408, -0.604),
    trackCompErr1 = cms.vdouble(5.093, 5.695, 4.607, 3.954),
    trackCompErr2 = cms.vdouble(0.547, 0.449, 0.461, 0.526),
    trackCompCutPattern = cms.vint32(3,5,6,9,10,12),   
    trackCompCutCurvMax = cms.vint32(34,34,34,34,34,34),   #this is shifted<<4
    trackCompCut        = cms.vint32(13,15,9,15,15,11),  
    chiSquareCutTight   = cms.vint32(25*20,50*20,30*20,126*20,126*20,30*20),  


    combos4=cms.vint32(9,10,11,12,13,14,15),
    combos3=cms.vint32(5,6,7),
    combos2=cms.vint32(3),
    combos1=cms.vint32(), #for future possible usage

    useOfflineAlgo = cms.bool(True),   

    mScatteringPhi = cms.vdouble(3.633, 0.0678, 0.0320, 0.0129),
    mScatteringPhiB = cms.vdouble(1.085, 0.552, 0.725, 0.750),
    pointResolutionPhi = cms.vdouble(27797., 599., 424., 190.),
    pointResolutionPhiB = cms.vdouble(13072., 10977., 15202., 11313.),
    pointResolutionVertex = cms.double(1.),

    ###Only for the offline algo -not in firmware --------------------
#    mScatteringPhi = cms.vdouble(2.49e-3,5.47e-5,3.49e-5,1.37e-5),
#    mScatteringPhi = cms.vdouble(64*2.49e-3,64*5.47e-5,64*3.49e-5,64*1.37e-5),
#    mScatteringPhiB = cms.vdouble(7.22e-3,3.461e-3,4.447e-3,4.12e-3),
#    pointResolutionPhi = cms.double(1.),
#    pointResolutionPhi = cms.double(64*1.),
#    pointResolutionPhiB = cms.double(500.),
#    pointResolutionVertex = cms.double(1.),

    # Total bits, signed
    bitsPhi = cms.int32(17),
    bitsPhiB = cms.int32(12),
    phiBScale = cms.int32(56),
    #    bitsPhiNew = cms.int32(17),
    #    bitsPhiOld = cms.int32(12),
    #    bitsPhiBNew = cms.int32(12),
    #    bitsPhiBOld = cms.int32(11),

)



simKBmtfDigis = cms.EDProducer("L1TMuonBarrelKalmanTrackProducer",
    src = cms.InputTag("simKBmtfStubs"),
    bx = cms.vint32(-2,-1,0,1,2),
#    bx = cms.vint32(0),
    algoSettings = bmtfKalmanTrackingSettings,
    trackFinderSettings = cms.PSet(
        sectorsToProcess = cms.vint32(0,1,2,3,4,5,6,7,8,9,10,11),
        verbose = cms.int32(0),
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
