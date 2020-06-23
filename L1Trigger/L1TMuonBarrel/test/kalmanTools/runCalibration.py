import ROOT
import itertools
import math
from DataFormats.FWLite import Events, Handle
from array import array
import pdb
import numpy
def median(lst):
    return numpy.median(numpy.array(lst))


PHILSB = 65536/0.8
PHIBLSB = 2048/1.4

def fetchSegmentsPhi(event,ontime=True,twinMux=True):
    phiSeg    = Handle  ('std::vector<L1MuCorrelatorHit>')
    if twinMux:
        event.getByLabel('simPhase2KBmtfStubs',phiSeg)
    else:
        event.getByLabel('simDtTriggerPrimitiveDigis',phiSeg)
    if ontime:
        filtered=filter(lambda x: x.bxNum()==0, phiSeg.product())
        return filtered
    else:
        return phiSeg.product()

def fetchSegmentsEta(event,ontime=True):
    thetaSeg  = Handle  ('std::vector<L1MuCorrelatorHit>')
    event.getByLabel('simPhase2KBmtfStubs',thetaSeg)
    if ontime:
        filtered=filter(lambda x: x.bxNum()==0, thetaSeg.product())
        return filtered
    else:
        return thetaSeg.product()    

def fetchGEANT(event):
    geantH  = Handle  ('vector<PSimHit>')
    event.getByLabel('g4SimHits:MuonDTHits',geantH)
    geant=filter(lambda x: x.pabs()>0.5 and abs(x.particleType())==13,geantH.product())
    return geant

def fetchGEN(event,etaMax=1.2):
    genH  = Handle  ('vector<reco::GenParticle>')
    event.getByLabel('genParticles',genH)
    genMuons=filter(lambda x: abs(x.pdgId())==13 and x.status()==1 and abs(x.eta())<etaMax,genH.product())
    return genMuons

def segINT(seg,f1=1,f2=1):
    return seg.phi()*f1,seg.phiB()*f2


def qPTInt(qPT,bits=17):
    lsb = lsBIT(bits)
    floatbinary = int(math.floor(abs(qPT)/lsb))
    return int((qPT/abs(qPT))*floatbinary)

def lsBIT(bits=17):
    maximum=1.25
    lsb = 1.25/pow(2,bits-1)
    return lsb


def getTrueCurvature(muon,geant,segments):
    thisMuonGEANT = filter(lambda x: (muon.charge()>0 and x.particleType()==-13) or ((muon.charge()<0) and x.particleType()==13),geant)
    energyInfo={1:[], 2:[],3:[],4:[]}
    qInfo={1:0.0, 2:0.0,3:0.0,4:0.0}
    qInfoINT={1:0, 2:0,3:0,4:0}
    for p in thisMuonGEANT:
        detid=ROOT.DTChamberId(p.detUnitId())
        station = detid.station()
        for s in segments:
            if s.depthRegion()==detid.station() and s.etaRegion()==detid.wheel() and s.phiRegion()==detid.sector()-1:
                energyInfo[station].append(p.pabs()*muon.pt()/muon.energy())
                break;

            
    for s in [1,2,3,4]:
        if len(energyInfo[s])==0:
            continue
        p = median(energyInfo[s])
        qInfo[s]=muon.charge()/p 
        qInfoINT[s] = qPTInt(qInfo[s], bits = 17)
    return qInfo,qInfoINT    

def matchTrack(muon,segments,geant):
    thisMuonGEANT = filter(lambda x: (muon.charge()>0 and x.particleType()==-13) or ((muon.charge()<0) and x.particleType()==13),geant)
    chambers=[]
    for p in thisMuonGEANT:        
        detid=ROOT.DTChamberId(p.detUnitId())
        chambers.append(p.detUnitId())
        
    chambers=list(set(chambers))


    assocSeg=[]   
    for s in segments:
        for c in chambers:
            detid=ROOT.DTChamberId(c)
            if s.etaRegion()==detid.wheel() and s.depthRegion()==detid.station() and s.phiRegion()==detid.sector()-1:
                if not (s in assocSeg):
                    assocSeg.append(s)

    return assocSeg


def log(nEvent, gen, stubs):
    print "Event {}".format(nEvent)
    print "GEN Muons"
    for g in gen:
        print "Gen mu pt={:.3f} eta={:.3f} phi={:.3f} charge={}".format(g.pt(), g.eta(), g.phi(), g.charge())
    print "STUBS"
    for s in stubs:
        print "stub bx={} depth={} etaRegion={} eta={} phiRegion={} phi={} phiB={} quality={}".format(s.bxNum(), s.depthRegion(), s.etaRegion(), s.eta(), s.phiRegion(), s.phi(), s.phiB(), s.quality())




events = Events([
    'root://cmseos.fnal.gov//store/user/bachtis/PhaseII_19_11_12/singleMu0_DTPhaseII.root',
]
)

def getStubPhi(seg):
    PHILSB = 65536/0.8
    sector = seg.phiRegion()
    phi = sector*math.pi/6 + seg.phi()/PHILSB
    while phi > math.pi:
        phi = phi-2*math.pi
    while phi < -math.pi:
        phi = 2*math.pi + phi
    return phi

def deltaPhi(p1, p2):
    delta = p1-p2
    while delta > math.pi:
        delta = delta-2*math.pi
    while delta < -math.pi:
        delta = 2*math.pi + delta
    return delta


stations=[1,2,3,4]
PHISCALE=pow(2,11)
PHIBSCALE=pow(2,9)
PHIFACTOR = 1
#PHIBFACTOR =8
PHIBFACTOR = 56
RELFACTOR = 1


initK = [-0.0628, -0.0869, -0.122, -0.272]
initK2 = [-1.385e-05, -2.985e-05, -1.402e-4, -4.923e-4]

DROR = {4:0.173*RELFACTOR,3:0.209*RELFACTOR,2:0.182*RELFACTOR}
DRORB = {4:(1+0.173),3:(1+0.209),2:(1+0.182)}
alpha = {4:-0.0523,3:-0.0793,2:-0.0619}
beta = {4:0.069,3:0.079,2:0.055}
aPhi = {4:0.0236, 3:0.03794, 2:0.037123, 1: 5.25100}
aPhiB = {4:-.35931, 3:-0.40417, 2:-.32815, 1: -3.7226}
aPhiBNLO = 3.9857e-5
trackComp = [-.5781,-.4224,-.24655,-.11516]
DRORCHI = {4: (726.-433.)/726. ,
           3: (619.-433.)/619. ,
           2: (512.-433.)/512.}


binsk = 256
maxk=32768


histos={}

offset={1:0.156,2:0.138,3:0.775,4:0.0}
offsetINV={1:0.207,2:0.,3:0.,4:0.0}

histos['phiProp']={}
histos['phiPropChi']={}
histos['phiBProp']={}
histos['curvFromPhiB']={}
histos['curvFromDPhi']={}
histos['phiBFromCurv']={}
histos['phiPropChiV']={}
histos['deltaPhiVsPhiB']={}
histos['deltaPhiVsK'] = {}
histos['deltaPhiBVsK'] = {}
histos['initKVsPhiB'] = {}
histos['compErr'] = {}
histos['curv'] = {}

for i,j in itertools.permutations([1,2,3,4],2):
    if not (i in histos['deltaPhiVsPhiB'].keys()):
        histos['deltaPhiVsPhiB'][i]={}
    histos['deltaPhiVsPhiB'][i][j]=ROOT.TH2D("deltaPhiVsPhiB_"+str(i)+"_"+str(j),"",256,-4*511,4*512,2048,-4*2047,4*2048)

    if not (i in histos['curvFromDPhi'].keys()):
        histos['curvFromDPhi'][i]={}
    histos['curvFromDPhi'][i][j]=ROOT.TH2D("curvFromDPhi_"+str(i)+"_"+str(j),"",512,-32*2047,32*2048,1024,-8192,8192)
    
    
for s in [1,2,3,4]:
    histos['curvFromPhiB'][s]=ROOT.TH2D("curvFromPhiB_"+str(s),"",256,-512,511,200,-10000,10000)
    histos['phiBFromCurv'][s]=ROOT.TH2D("phiBFromCurv_"+str(s),"",64,-512,511,128,-511,512)
    histos['phiProp'][s]=ROOT.TH2D("phiProp_"+str(s),"",binsk,-maxk,maxk,100,-2000,2000)
    histos['phiPropChiV'][s]=ROOT.TH2D("phiPropChiV_"+str(s),"",binsk,-maxk,maxk,50,-16*200,16*200)
    histos['phiPropChi'][s]=ROOT.TH2D("phiPropChi_"+str(s),"",binsk,-3000,3000,50,-16*200,16*200)
    histos['phiBProp'][s]=ROOT.TH2D("phiBProp_"+str(s),"",binsk/2-1,-maxk,maxk,100,-4*2000,4*2000)
    if s != 1:
        histos['deltaPhiVsK'][s] = ROOT.TH2D("deltaPhiVsK_"+str(s),"", binsk,-maxk,maxk,256,-511,511)
        histos['deltaPhiBVsK'][s] = ROOT.TH2D("deltaPhiBVsK_"+str(s),"", binsk,-maxk,maxk,256,-2000,2000)
    else:
        histos['deltaPhiVsK'][s] = ROOT.TH2D("deltaPhiVsK_"+str(s),"", binsk,-maxk,maxk,256,-2048,2048)
        histos['deltaPhiBVsK'][s] = ROOT.TH2D("deltaPhiBVsK_"+str(s),"", binsk,-maxk,maxk,256,-8192,8192)

    histos['initKVsPhiB'][s] = ROOT.TH2D("initK_{}".format(s), "", 1024, -4*512, 4*511, 400, -4*400, 4*400)
    histos['compErr'][s] = ROOT.TH2D("compErr_{}".format(s), "", 128, -maxk/8, maxk/8, 256, -1024, 1023)
    histos['curv'][s] = ROOT.TH1D("curv_{}".format(s), "", 2048, -4096, 4096)

vertexPhi = ROOT.TH2D("vertexPhi", "",300 , -15000, 15000, 200, -2**16, 2**16)
vertexPhiB = ROOT.TH2D("vertexPhiB", "", binsk/4, -maxk, maxk, 50, -2048*32, 2048*32)
vertexELoss = ROOT.TH2D("vertexELoss", "", binsk, -maxk,maxk,binsk,-maxk,maxk)
phiAt2 = ROOT.TH2D("phiAt2", "", binsk,-maxk,maxk, 1024, -4*512,4*512)    

N=0
for event in events:
    N=N+1
    if N%10000==0:
        print "Processed {} events".format(N)
    #if N==100000:
    #    break;
    genMuons=fetchGEN(event)
    segments=fetchSegmentsPhi(event)
    segmentsTheta=fetchSegmentsEta(event)
    geant=fetchGEANT(event)
    segmentsTheta=sorted(segmentsTheta,key=lambda x: x.depthRegion())

    
    for g in genMuons:
        trueK,trueKINT = getTrueCurvature(g,geant,segments)
        cotTheta = int(g.eta()/0.010875)
        segTheta=matchTrack(g,segmentsTheta,geant)
        seg=matchTrack(g,segments,geant)

        for s in seg:
            phi,phiB=segINT(s,PHIFACTOR,PHIBFACTOR)
            histos['curvFromPhiB'][s.depthRegion()].Fill(s.phiB(),trueKINT[s.depthRegion()])
            kReco = s.phiB()*initK[s.depthRegion()-1]/(1+initK2[s.depthRegion()-1]*abs(s.phiB()))
            deltaK = kReco - trueKINT[s.depthRegion()]
            histos['initKVsPhiB'][s.depthRegion()].Fill(s.phiB(), deltaK)
#            histos['phiBFromCurv'][s.stNum()].Fill(trueKINT[s.stNum()]>>4,phiB)
            histos['phiBFromCurv'][s.depthRegion()].Fill(qPTInt(g.charge()/g.pt())>>4,s.phiB())

            comp = trackComp[s.depthRegion()-1]*(qPTInt(g.charge()/g.pt())>>4)
            histos['compErr'][s.depthRegion()].Fill(qPTInt(g.charge()/g.pt())>>4, s.phiB()-comp)
            histos['curv'][s.depthRegion()].Fill(trueKINT[s.depthRegion()])

            if s.depthRegion() == 1:
                vertexPhiB.Fill(trueKINT[s.depthRegion()], phiB)
                stubPhi = getStubPhi(s)
                stubPhiB = s.phiB()/PHIBLSB
                temp = g.phi() - stubPhi - stubPhiB
                temp = int(temp*PHILSB)
                vertexPhi.Fill(trueKINT[s.depthRegion()], temp), 
                vertexELoss.Fill(trueKINT[s.depthRegion()],qPTInt(g.charge()/g.pt()))
                
                kInt = trueKINT[s.depthRegion()]
                propPhi = phi+aPhi[1]*kInt+phiB
                propPhi_full = propPhi/PHILSB + s.phiRegion()*math.pi/6
                deltaPhi_full = deltaPhi(g.phi(), propPhi_full)
                dPhi = deltaPhi_full*PHILSB
                propPhiB = aPhiB[1]*(kInt/2.)/(1+aPhiBNLO*abs(kInt/2.))-phiB
                histos['deltaPhiVsK'][1].Fill(trueKINT[s.depthRegion()], dPhi)
                histos['deltaPhiBVsK'][1].Fill(trueKINT[s.depthRegion()], propPhiB)
#                pdb.set_trace()
        for s1,s2 in itertools.permutations(seg,2):
            phi1,phiB1=segINT(s1,PHIFACTOR,PHIBFACTOR)
            phi2,phiB2 = segINT(s2,PHIFACTOR,PHIBFACTOR)

            if (s2.phiRegion()==s1.phiRegion()+1) or (s1.phiRegion()==11 and s2.phiRegion()==0) :
                phi2=phi2+42893
                continue
            if (s2.phiRegion()==s1.phiRegion()-1) or (s1.phiRegion()==0 and s2.phiRegion()==11) :
                phi2=phi2-42893
                continue                
            
            
            if s1.quality()>5 and (s1.depthRegion()!=s2.depthRegion()):
                histos['deltaPhiVsPhiB'][s1.depthRegion()][s2.depthRegion()].Fill(s1.phiB(),phi2-phi1)
                histos['curvFromDPhi'][s1.depthRegion()][s2.depthRegion()].Fill(phi2-phi1,qPTInt(g.charge()/g.pt()))

            if s1.depthRegion()+1==s2.depthRegion():                
                st=s2.depthRegion()    
                qPT=trueKINT[st]
                
                propPhi = phi2-phiB2*DROR[st]+aPhi[st]*qPT    
                propPhiB =DRORB[st]*phiB2+aPhiB[st]*qPT
                dPhi = propPhi-phi1
                dPhiB = propPhiB-phiB1
                histos['deltaPhiVsK'][st].Fill(trueKINT[s2.depthRegion()], dPhi)
                histos['deltaPhiBVsK'][st].Fill(trueKINT[s2.depthRegion()], dPhiB)
                
                histos['phiProp'][s2.depthRegion()].Fill(trueKINT[s2.depthRegion()],(phi1-phi2)+DROR[s2.depthRegion()]*phiB2)
                histos['phiBProp'][s2.depthRegion()].Fill(trueKINT[s2.depthRegion()],phiB1-DRORB[s2.depthRegion()]*phiB2)


                # for chi 2 lookmonly from station 1 -> 2,3,4
            if s1.depthRegion()==1 and s2.depthRegion()!=1: 
                #histos['phiPropChi'][s2.depthRegion()].Fill(trueKINT[s1.depthRegion()],(phi2-phi1)+DRORCHI[s2.depthRegion()]*phiB1)
                histos['phiPropChi'][s2.depthRegion()].Fill(trueKINT[s1.depthRegion()],(phi2-phi1)+(phiB2-phiB1))
                histos['phiPropChiV'][s2.depthRegion()].Fill(qPTInt(g.charge()/g.pt()),(phi2-phi1))
            if s1.depthRegion()==1 and s2.depthRegion()==2:
                phiAt2.Fill(phiB1, phi2-phi1)
                
                
f=ROOT.TFile("calibrationConstants_singleMu0_DTPhaseII.root","RECREATE")
vertexPhi.Write()
vertexPhiB.Write()
vertexELoss.Write()
phiAt2.Write()
for s in [4,3,2,1]:
    histos['phiProp'][s].Write()
    histos['phiPropChi'][s].Write()
    histos['phiPropChiV'][s].Write()

    histos['phiBProp'][s].Write()
    histos['curvFromPhiB'][s].Write()
    histos['phiBFromCurv'][s].Write()
    
    histos['deltaPhiVsK'][s].Write()
    histos['deltaPhiBVsK'][s].Write()
    
    histos['initKVsPhiB'][s].Write()
    histos['compErr'][s].Write()
    histos['curv'][s].Write()
for i,j in itertools.permutations([1,2,3,4],2):
    histos['deltaPhiVsPhiB'][i][j].Write()
    histos['curvFromDPhi'][i][j].Write()

    
f.Close()
