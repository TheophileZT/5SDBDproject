module.exports = {
    async rewrites() {
      return [
        {
          source: "/api/:path*", // Route API locale
          destination: "http://inference:5000/:path*", // Proxy vers le backend Flask
        },
      ];
    },
  };