{
  description = "Consistent storage for net-synergy projects.";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, poetry2nix }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs {
        inherit system;
        overlays = [ poetry2nix.overlays.default ];
      };

      synstoreEnv = pkgs.poetry2nix.mkPoetryEnv {
        projectDir = ./.;
        editablePackageSources = { synstore = ./.; };
        preferWheels = true;
      };
    in {
      devShells.${system}.default =
        pkgs.mkShell { packages = [ synstoreEnv pkgs.poetry ]; };
    };
}
