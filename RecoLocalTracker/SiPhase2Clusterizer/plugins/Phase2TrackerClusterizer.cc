#include "RecoLocalTracker/SiPhase2Clusterizer/plugins/Phase2TrackerClusterizer.h"

#include "Geometry/CommonDetUnit/interface/GeomDetUnit.h"
#include "Geometry/Records/interface/TrackerDigiGeometryRecord.h"
#include "Geometry/TrackerGeometryBuilder/interface/TrackerGeometry.h"
#include "Geometry/TrackerGeometryBuilder/interface/PixelGeomDetUnit.h"

#include "DataFormats/Common/interface/DetSetVector.h"
#include "DataFormats/Phase2TrackerDigi/interface/Phase2TrackerDigi.h"

#include "FWCore/PluginManager/interface/ModuleDef.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Framework/interface/ESHandle.h"

#include <vector>
#include <iostream>


    /*
     * Initialise the producer
     */ 

    Phase2TrackerClusterizer::Phase2TrackerClusterizer(edm::ParameterSet const& conf) :
        clusterizer_(new Phase2TrackerClusterizerAlgorithm(conf.getParameter< unsigned int >("maxClusterSize"), conf.getParameter< unsigned int >("maxNumberClusters"))),
        token_(consumes< edm::DetSetVector< Phase2TrackerDigi > >(conf.getParameter<edm::InputTag>("src"))) {
            produces< Phase2TrackerCluster1DCollectionNew >(); 
    }

    Phase2TrackerClusterizer::~Phase2TrackerClusterizer() { }

    /*
     * Clusterize the events
     */

    void Phase2TrackerClusterizer::produce(edm::StreamID sid, edm::Event& event, const edm::EventSetup& eventSetup) const {

        // Get the Digis
        edm::Handle< edm::DetSetVector< Phase2TrackerDigi > > digis;
        event.getByToken(token_, digis);
        
        // Get the geometry
        edm::ESHandle< TrackerGeometry > geomHandle;
        eventSetup.get< TrackerDigiGeometryRecord >().get(geomHandle);
        const TrackerGeometry* tkGeom(&(*geomHandle)); 

        // Global container for the clusters of each modules
        std::auto_ptr< Phase2TrackerCluster1DCollectionNew > outputClusters(new Phase2TrackerCluster1DCollectionNew());

        // Go over all the modules
        for (edm::DetSetVector< Phase2TrackerDigi >::const_iterator DSViter = digis->begin(); DSViter != digis->end(); ++DSViter) {

            DetId detId(DSViter->detId());

            // Geometry
            const GeomDetUnit* geomDetUnit(tkGeom->idToDetUnit(detId));
            const PixelGeomDetUnit* pixDet = dynamic_cast< const PixelGeomDetUnit* >(geomDetUnit);
            if (!pixDet) assert(0);

            // Container for the clusters that will be produced for this modules
            edmNew::DetSetVector< Phase2TrackerCluster1D >::FastFiller clusters(*outputClusters, DSViter->detId());

            // Setup the clusterizer algorithm for this detector (see ClusterizerAlgorithm for more details)
            clusterizer_->setup(pixDet);

            // Pass the list of Digis to the main algorithm
            // This function will store the clusters in the previously created container
            clusterizer_->clusterizeDetUnit(*DSViter, clusters);

            if (clusters.empty()) clusters.abort();
        }

        // Add the data to the output
        outputClusters->shrink_to_fit();
        event.put(outputClusters);
    }

DEFINE_FWK_MODULE(Phase2TrackerClusterizer);
