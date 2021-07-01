import FWCore.ParameterSet.Config as cms
import FWCore.Utilities.FileUtils as FileUtils
import FWCore.PythonUtilities.LumiList as LumiList
import FWCore.ParameterSet.Types as CfgTypes

process = cms.Process("TSPA")

process.load("FWCore.MessageService.MessageLogger_cfi")
#if more events are activated, choose to print every 1000:
#process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
             'root://eospublic.cern.ch//eos/opendata/cms/Run2012B/DoubleMuParked/AOD/22Jan2013-v1/10000/1EC938EF-ABEC-E211-94E0-90E6BA442F24.root'
            #'file:/playground/1EC938EF-ABEC-E211-94E0-90E6BA442F24.root'
            #'root://eospublic.cern.ch//eos/opendata/cms/MonteCarlo2012/Summer12_DR53X/TTbar_8TeV-Madspin_aMCatNLO-herwig/AODSIM/PU_S10_START53_V19-v2/00000/000A9D3F-CE4C-E311-84F8-001E673969D2.root'
          
    )
)

#needed to get the actual prescale values used from the global tag
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
#process.GlobalTag.connect = cms.string('sqlite_file:/cvmfs/cms-opendata-conddb.cern.ch/FT_53_LV5_AN1_RUNA.db')
process.GlobalTag.globaltag = 'FT_53_LV5_AN1::All'

#configure the analyzer
#inspired by https://github.com/cms-sw/cmssw/blob/CMSSW_5_3_X/HLTrigger/HLTfilters/interface/HLTHighLevel.h
process.gettriggerinfo = cms.EDAnalyzer('TriggerSimplePrescalesAnalyzer',
                              processName = cms.string("HLT"),
                              triggerPatterns = cms.vstring("HLT_DoubleMu5_IsoMu5_v*","HLT_Mu13_Mu8_v*", "HLT_Mu22_TkMu22_v*"), #if left empty, all triggers will run        
                              triggerResults = cms.InputTag("TriggerResults","","HLT"),
                              triggerEvent   = cms.InputTag("hltTriggerSummaryAOD","","HLT")                             
                              )

process.TFileService = cms.Service(
    "TFileService", fileName=cms.string("myoutput.root"))

process.triggerinfo = cms.Path(process.gettriggerinfo)
process.schedule = cms.Schedule(process.triggerinfo)
