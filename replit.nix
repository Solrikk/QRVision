{ pkgs }: {
  deps = [
    pkgs.glibcLocales
    pkgs.python310Full
    pkgs.zbar
    pkgs.poetry
    pkgs.python310Full
    pkgs.python310Packages.opencv4
    pkgs.ffmpeg
    pkgs.libv4l
    pkgs.v4l-utils
  ];

  env = {
    LC_ALL = "en_US.utf8";
    LANG = "en_US.utf8";
    LD_LIBRARY_PATH = "${pkgs.zbar}/lib:${placeholder ''LD_LIBRARY_PATH''}";
  };
}