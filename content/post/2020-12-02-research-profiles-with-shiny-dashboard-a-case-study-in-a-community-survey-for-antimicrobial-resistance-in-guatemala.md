---
title: 'Research profiles with Shiny Dashboard: A case study in a community survey
  for antimicrobial resistance in Guatemala'
author: Juan Carlos Romero
date: '2020-12-02'
tags:
  - Research Profiles
  - shiny
slug: research-profiles-with-shiny-dashboard-a-case-study-in-a-community-survey-for-antimicrobial-resistance-in-guatemala
---

October 28th, 2020.

_By Juan Carlos Romero (jromero@ces.uvg.edu.gt), Juan Pablo Alvis (jalvis@ces.uvg.edu.gt), Laura María Grajeda (lgrajeda@ces.uvg.edu.gt) from Centro de Estudios en Salud, Universidad del Valle de Guatemala._

The successful implementation of community surveys requires close and timely monitoring of study activities. To monitor the performance of an antimicrobial resistance two-stage cluster survey in communities of the highlands of Guatemala, we developed a web-based application with R Shiny dashboards. Our password-protected application displays study progress indicators, approaching activities, and unresolved data quality issues using maps, tables, graphics, dynamic texts and downloadable spreadsheets. Scientists use this information to assess study performance against upcoming milestones, to address deviations in a timely manner, to assist real-time planning of field activities and to serve as a communication tool within the study team and with funding organizations.

We captured geographic data with GPS devices, and demographic, clinical and laboratory data with the RedCap system. All data was stored in a SQL-structured database. An ecosystem of scripts, each dedicated to a particular map, table or graphic of the dashboard, produces data structures ready to for R packages to create each object. We programmed the process to be repeated at 12-hour intervals to feed the Shiny dashboard with updated data and reduce loading time. We published the dashboard using the Shiny server open-source platform in a dedicated Linux server accessed by an intranet IP. To facilitate collaborative work in creating and maintaining the dashboard, we implemented the Apache Subversion in a centralized server for code control and the open-source Tortoise SVN client for version control.

A description of our approach to create a Shiny Dashboard and a discussion of alternatives follow in the video. Comments and discussion are very welcome.

YouTube Link: <https://youtu.be/GryIw3OHXyc>
