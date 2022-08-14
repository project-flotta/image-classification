FROM python:3.7-alpine

ENV PYTHONUNBUFFERED=1

RUN echo -e '@edgunity http://nl.alpinelinux.org/alpine/edge/community\n\
@edge http://nl.alpinelinux.org/alpine/edge/main\n\
@testing http://nl.alpinelinux.org/alpine/edge/testing\n\
@community http://dl-cdn.alpinelinux.org/alpine/edge/community'\
  >> /etc/apk/repositories

RUN apk add --update --no-cache --virtual=build-dependencies \
      build-base \
      openblas-dev \
      unzip \
      wget \
      cmake \
      libtbb  \
      libtbb-dev \
      libjpeg  \
      libjpeg-turbo-dev \
      libpng-dev \
      tiff-dev \
      libwebp-dev \
      clang-dev \
      linux-headers \
      && pip install -U --no-cache-dir numpy

ENV CC /usr/bin/clang
ENV CXX /usr/bin/clang++
ENV OPENCV_VERSION=4.6.0

RUN mkdir -p /opt && cd /opt && \
  wget https://github.com/opencv/opencv/archive/${OPENCV_VERSION}.zip && \
  unzip ${OPENCV_VERSION}.zip && \
  rm -rf ${OPENCV_VERSION}.zip

RUN mkdir -p /opt/opencv-${OPENCV_VERSION}/build && \
  cd /opt/opencv-${OPENCV_VERSION}/build && \
  cmake \
  -D CMAKE_BUILD_TYPE=RELEASE \
  -D CMAKE_INSTALL_PREFIX=/usr/local \
  -D WITH_FFMPEG=NO \
  -D WITH_IPP=NO \
  -D WITH_OPENEXR=NO \
  -D WITH_TBB=YES \
  -D BUILD_EXAMPLES=NO \
  -D BUILD_ANDROID_EXAMPLES=NO \
  -D INSTALL_PYTHON_EXAMPLES=NO \
  -D BUILD_DOCS=NO \
  -D BUILD_opencv_python2=NO \
  -D BUILD_opencv_python3=ON \
  -D PYTHON3_EXECUTABLE=/usr/local/bin/python \
  -D PYTHON3_INCLUDE_DIR=/usr/local/include/python3.7m/ \
  -D PYTHON3_LIBRARY=/usr/local/lib/libpython3.so \
  -D PYTHON_LIBRARY=/usr/local/lib/libpython3.so \
  -D PYTHON3_PACKAGES_PATH=/usr/local/lib/python3.7/site-packages/ \
  -D PYTHON3_NUMPY_INCLUDE_DIRS=/usr/local/lib/python3.7/site-packages/numpy/core/include/ \
  .. && \
  make && \
  make install && \
  rm -rf /opt/opencv-${OPENCV_VERSION} && \
  apk del build-dependencies && \
  rm -rf /var/cache/apk/*

# allows to run bash (remove me)
RUN apk add --update bash --no-cache
# runtime dependencies
RUN apk add --update --no-cache openblas libstdc++ libtbb libjpeg libwebp libpng libtiffxx

RUN mkdir /app
WORKDIR /app

COPY . .

#RUN python -m venv env && source ./env/bin/activate && \
#    pip install --upgrade pip setuptools && \
#    pip install --no-cache-dir opencv-python

# RUN pip install --no-cache-dir -r requirements.txt

ENV PATH="/py/bin:$PATH"

CMD ["python3" , "main.py"]