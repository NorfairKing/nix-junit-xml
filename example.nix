let pkgs = import <nixpkgs> {};
in {
  succeeding = pkgs.writeText "hello" "hello-world";
  failing = pkgs.runCommand "false"{} "false";
}
