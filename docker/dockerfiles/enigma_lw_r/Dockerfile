FROM ghcr.io/rocker-org/tidyverse:4.5.3

ENV TZ=Europe
ENV DEBIAN_FRONTEND=noninteractive

RUN R -q -e "install.packages(c('fmsb','glmnet','PerformanceAnalytics','caret','tidymodels','splitstackshape','fastDummies','pbapply','lme4','lmerTest','kernlab'), repos='https://packagemanager.posit.co/cran/__linux__/noble/2026-04-21')"
