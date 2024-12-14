interface Robot {
  x: number;
  y: number;
  dx: number;
  dy: number;
}

async function parse_input(filePath: string): Promise<Robot[]> {
  const content = await Deno.readTextFile(filePath);
  const robots: Robot[] = [];
  for (const line of content.trim().split("\n")) {
    const [pos, vel] = line.split(" ");
    const [x, y] = pos.substring(2).split(",").map(Number);
    const [dx, dy] = vel.substring(2).split(",").map(Number);
    robots.push({
      x,
      y,
      dx,
      dy,
    });
  }
  return robots;
}

function new_location(
  robot: Robot,
  seconds: number,
  height: number,
  width: number,
): number[] {
  return [
    (robot.x + robot.dx * seconds + width * seconds) % width,
    (robot.y + robot.dy * seconds + height * seconds) % height,
  ];
}

function quadrant_product(
  robots: Robot[],
  seconds: number,
  height: number,
  width: number,
): number {
  const quadrant_counts = [0, 0, 0, 0];
  for (const robot of robots) {
    const loc = new_location(robot, seconds, height, width);
    if (loc[0] > (width - 1) / 2) {
      if (loc[1] < (height - 1) / 2) {
        quadrant_counts[0]++;
      } else if (loc[1] > (height - 1) / 2) {
        quadrant_counts[3]++;
      }
    } else if (loc[0] < (width - 1) / 2) {
      if (loc[1] < (height - 1) / 2) {
        quadrant_counts[1]++;
      } else if (loc[1] > (height - 1) / 2) {
        quadrant_counts[2]++;
      }
    }
  }
  return quadrant_counts.reduce((a, b) => a * b, 1);
}

function get_variance(robots: Robot[]): number {
  const x_mean = robots.reduce((sum, robot) => sum + robot.x, 0) /
    robots.length;
  const y_mean = robots.reduce((sum, robot) => sum + robot.y, 0) /
    robots.length;
  const x_variance = robots.reduce((sum, robot) => {
    const diff = robot.x - x_mean;
    return sum + diff * diff;
  }, 0) / robots.length;
  const y_variance = robots.reduce((sum, robot) => {
    const diff = robot.y - y_mean;
    return sum + diff * diff;
  }, 0) / robots.length;
  return x_variance * y_variance;
}

function min_variance(robots: Robot[], height: number, width: number): number {
  let variance = get_variance(robots);
  let variance_time = 0;
  for (let i = 1; i < height * width; i++) {
    for (let j = 0; j < robots.length; j++) {
      [robots[j].x, robots[j].y] = new_location(robots[j], 1, height, width);
    }
    const new_variance = get_variance(robots);
    if (new_variance < variance) {
      variance = new_variance;
      variance_time = i;
    }
  }
  return variance_time;
}

if (import.meta.main) {
  const filePath = Deno.args[0];
  if (!filePath) {
    console.error("Please provide a file path as an argument");
    Deno.exit(1);
  }

  try {
    const height = 103;
    const width = 101;
    const time = 100;
    const robots = await parse_input(filePath);
    console.log(
      `The safety factor after 100 seconds is ${
        quadrant_product(robots, time, height, width)
      }.`,
    );
    console.log(
      `The Christmas tree appears after ${
        min_variance(robots, height, width)
      } seconds.`,
    );
  } catch (error) {
    console.error("Error reading file:", (error as Error).message);
    Deno.exit(1);
  }
}
