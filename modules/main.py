import os
import math
import json
import re
import shutil

class OsuMap:
	def __init__ (self, general, editor, metadata, difficulty, events, timingpoints, colors, hitobjects):
		self.general = general
		self.editor = editor
		self.metadata = metadata
		self.difficulty = difficulty
		self.events = events
		self.timingpoints = timingpoints
		self.colors = colors
		self.hitobjects = hitobjects

def ParseAllBeatmapData(osufile):
	# General
	depth = 0
	linepos = 0
	DataGeneral = []
	for line in osufile:
		linepos += 1
		if line == "[General]":
			depth = linepos
		elif line == "[Editor]":
			# print(f"{depth+1} until {linepos-2}")
			searchdepthstart = depth+1
			searchdepthend = linepos-2
			for i in range(searchdepthstart-1, searchdepthend-1):
				DataGeneral.append(osufile[i])
			break
	# Editor
	depth = 0
	linepos = 0
	DataEditor = []
	for line in osufile:
		linepos += 1
		if line == "[Editor]":
			depth = linepos
		elif line == "[Metadata]":
			# print(f"{depth+1} until {linepos-2}")
			searchdepthstart = depth+1
			searchdepthend = linepos-2
			for i in range(searchdepthstart-1, searchdepthend-1):
				DataEditor.append(osufile[i])
			break
	# Metadata
	depth = 0
	linepos = 0
	DataMetadata = []
	for line in osufile:
		linepos += 1
		if line == "[Metadata]":
			depth = linepos
		elif line == "[Difficulty]":
			# print(f"{depth+1} until {linepos-2}")
			searchdepthstart = depth+1
			searchdepthend = linepos-2
			for i in range(searchdepthstart-1, searchdepthend-1):
				DataMetadata.append(osufile[i])
			break	# Events

	# Difficulty
	depth = 0
	linepos = 0
	DataDifficulty = []
	for line in osufile:
		linepos += 1
		if line == "[Difficulty]":
			depth = linepos
		elif line == "[Events]":
			# print(f"{depth+1} until {linepos-2}")
			searchdepthstart = depth+1
			searchdepthend = linepos-2
			for i in range(searchdepthstart-1, searchdepthend-1):
				DataDifficulty.append(osufile[i])
			break	
	# Events
	depth = 0
	linepos = 0
	DataEvents = []
	for line in osufile:
		linepos += 1
		if line == "[Events]":
			depth = linepos
		elif line == "[TimingPoints]":
			# print(f"{depth+1} until {linepos-2}")
			searchdepthstart = depth+1
			searchdepthend = linepos-2
			for i in range(searchdepthstart-1, searchdepthend-1):
				DataEvents.append(osufile[i])
			break	

	# TimingPoints
	depth = 0
	linepos = 0
	DataTimingPoints = []
	for line in osufile:
		linepos += 1
		if line == "[TimingPoints]":
			depth = linepos
		elif line == "[Colours]":
			# print(f"{depth+1} until {linepos-2}")
			searchdepthstart = depth+1
			searchdepthend = linepos-2
			for i in range(searchdepthstart-1, searchdepthend-1):
				DataTimingPoints.append(osufile[i])
			break

	# Colours
	depth = 0
	linepos = 0
	DataColours = []
	for line in osufile:
		linepos += 1
		if line == "[Colours]":
			depth = linepos
		elif line == "[HitObjects]":
			# print(f"{depth+1} until {linepos-2}")
			searchdepthstart = depth+1
			searchdepthend = linepos-2
			for i in range(searchdepthstart-1, searchdepthend-1):
				DataColours.append(osufile[i])
			break
	# HitObjects
	depth = 0
	linepos = 0
	DataHitObjects = []
	for line in osufile:
		linepos += 1
		if line == "[HitObjects]":
			depth = linepos
			searchdepthstart = depth+1
			searchdepthend = len(osufile)
			for i in range(searchdepthstart-1, searchdepthend-1):
				DataHitObjects.append(osufile[i])
			break
	osudata = OsuMap(DataGeneral, DataEditor, DataMetadata, DataDifficulty, DataEvents, DataTimingPoints, DataColours, DataHitObjects) 
	return osudata

def MergeAll(param):
	i = 0
	for osu in re.split("\n", param):
		if i == 0:
			MergeTwo(osu, re.split("\n", param)[1])
		elif i > 2:
			metadata = ParseAllBeatmapData(osu)
			artist = re.split(":",metadata.metadata[2])[1]
			title = re.split(":",metadata.metadata[0])[1]
			mapper = re.split(":",metadata.metadata[4])[1]
			MergeTwo(osu, f"{artist} - {title} ({mapper}) [Result].osu")
		i += 1

def MergeTwo(osufile1, osufile2):
	osufile1file = open(osufile1, encoding="utf-8").read().splitlines()
	osufile2file = open(osufile2, encoding="utf-8").read().splitlines()
	osufile1 = ParseAllBeatmapData(open(osufile1, encoding="utf-8").read().splitlines())
	osufile2 = ParseAllBeatmapData(open(osufile2, encoding="utf-8").read().splitlines())
	artist = re.split(":",osufile1.metadata[2])[1]
	title = re.split(":",osufile1.metadata[0])[1]
	mapper = re.split(":",osufile1.metadata[4])[1]
	open(f"{artist} - {title} ({mapper}) [Result].osu", 'a').close()
	resultfile = open(f"{artist} - {title} ({mapper}) [Result].osu", "w", encoding="utf-8")
	towrite = ""
	towrite += "[General]\n"
	for line in osufile1.general:
		towrite += line + "\n"
	towrite += "\n[Editor]\n"
	for line in osufile1.editor:
		towrite += line + "\n"
	towrite += "\n[Metadata]\n"
	for line in osufile1.metadata:
		if not line.startswith("Version"):
			towrite += line + "\n"
		else:
			towrite += "Version:Result" + "\n"
	towrite += "\n[Difficulty]\n"
	for line in osufile1.difficulty:
		towrite += line + "\n"
	towrite += "\n[Events]\n"
	for line in osufile1.events:
		towrite += line + "\n"
	towrite += "\n[TimingPoints]\n"
	alltimingpoints = []
	for line in osufile1.timingpoints:
		alltimingpoints.append(line)
	for line2 in osufile2.timingpoints:
		alltimingpoints.append(line2)
	notduplicatedline = list(dict.fromkeys(alltimingpoints))
	for line in notduplicatedline:
		towrite += line + "\n"
	towrite += "\n[Colours]\n"
	for line in osufile1.colors:
		towrite += line + "\n"
	towrite += "\n[HitObjects]\n"
	for line in osufile1.hitobjects:
		towrite += line + "\n"
	for line in osufile2.hitobjects:
		towrite += line + "\n"	
	resultfile.write(towrite)
