// Renders case images: official brand logos (simple-icons) and pictograms (react-icons) to PNG.
const fs = require("fs");
const sharp = require("sharp");
const React = require("react");
const { renderToStaticMarkup } = require("react-dom/server");
const si = require("simple-icons");

const logos = { airbnb: "airbnb", uber: "uber", dropbox: "dropbox", tesla: "tesla", m3: "3m", ge: "generalelectric", mcd: "mcdonalds", nasa: "nasa", yc: "ycombinator", apple: "apple" };
const icons = {
  juicero: ["md", "MdBlender", "6B8E23"], tada: ["fa", "FaShuttleVan", "1A1A1A"], quibi: ["md", "MdOndemandVideo", "7A3DB8"],
  webvan: ["fa", "FaTruck", "C0504D"], zappos: ["gi", "GiRunningShoe", "17869E"], nsf: ["md", "MdScience", "002060"],
  nespresso: ["fa", "FaMugHot", "5C3A21"], baemin: ["fa", "FaMotorcycle", "2AC1BC"], spanx: ["fa", "FaPiggyBank", "D9668A"],
  cirque: ["fa", "FaTheaterMasks", "1F3A93"], wii: ["fa", "FaGamepad", "4A4A4A"], factory: ["md", "MdFactory", "002060"],
  mit: ["fa", "FaUniversity", "A31F34"], bluebottle: ["gi", "GiCoffeeBeans", "2B6CB0"], postit: ["fa", "FaStickyNote", "E3B900"],
};

(async () => {
  const all = Object.values(si).filter((x) => x && x.slug);
  for (const [k, slug] of Object.entries(logos)) {
    const ic = all.find((x) => x.slug === slug);
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="#${ic.hex}" d="${ic.path}"/></svg>`;
    await sharp(Buffer.from(svg), { density: 600 }).resize(400, 400, { fit: "contain", background: { r: 0, g: 0, b: 0, alpha: 0 } }).png().toFile(`img/${k}.png`);
  }
  for (const [k, [lib, name, hex]] of Object.entries(icons)) {
    const C = require("react-icons/" + lib)[name];
    const svg = renderToStaticMarkup(React.createElement(C, { size: 400, color: "#" + hex }));
    await sharp(Buffer.from(svg)).resize(400, 400, { fit: "contain", background: { r: 0, g: 0, b: 0, alpha: 0 } }).png().toFile(`img/${k}.png`);
  }
  console.log(fs.readdirSync("img").join(" "));
})();
