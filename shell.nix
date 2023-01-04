let
  pkgs = import <nixpkgs> {};
  pythonEnv = pkgs.python3.withPackages (p: with p; [
    junit-xml
  ]);
in pkgs.mkShell {
  name = "nix-junit-xml-shell";
  buildInputs = with pkgs; [
    pythonEnv
  ];
}
