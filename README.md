## MrfzDataVisualize

- Currently supports Arknights agents and news Kibana dashboard for data visiualizing
- Supports saving the images and data locally as well

### Setup
Setting up the environment and dashboards
- `python3 -m pip install -r requirements.txt`
- `cd config && docker compose up -d`

### Get started
Get a list of the supported operations with `python3 start.py --help`
<br/>
- Initialize dashboards and data for arknights news `python3 start.py --mode prod --save_img true --task crawl news`
- To sync and get the latest updates from arknights new `python3 start.py --mode prod --save_img true --task sync news`
- Similarly, for agents sync `python3 start.py --mode dev --save_img false --task sync agent` 

### Arknights News Mapping

[NewsMapping.md](https://github.com/TyroneHe-0926/MrfzDataVisualize/blob/main/crawler/news/README.md)

### Arknights Agents Mapping

[AgentsMapping.md](https://github.com/TyroneHe-0926/MrfzDataVisualize/blob/main/crawler/agents/README.md)

### Sample News Dashboard

![Dashboard Screenshot](https://github.com/TyroneHe-0926/MrfzDataVisualize/blob/main/assets/news-dashboard.png?raw=true)

### Sample Agent Info Dashboards

![Dashboard Screenshot](https://github.com/TyroneHe-0926/MrfzDataVisualize/blob/main/assets/agents-info-dashboard-1.jpeg?raw=true)

![Dashboard Screenshot](https://github.com/TyroneHe-0926/MrfzDataVisualize/blob/main/assets/agents-info-dashboard-2.jpeg?raw=true)

### Sample Agent Spec Dashboards

![Dashboard Screenshot](https://github.com/TyroneHe-0926/MrfzDataVisualize/blob/main/assets/agents-spec-dashboard-1.jpeg?raw=true)

![Dashboard Screenshot](https://github.com/TyroneHe-0926/MrfzDataVisualize/blob/main/assets/agents-spec-dashboard-2.jpeg?raw=true)
